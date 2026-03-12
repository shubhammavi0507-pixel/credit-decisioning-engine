import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import asyncio
from pathlib import Path
import uuid
import json

# Import our modules
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ingestion.pdf_extractor import PDFExtractor
from src.ingestion.feature_engineering import FeatureEngineer
from src.research.web_researcher import WebResearcher
from src.ml_engine.credit_model import CreditDecisionModel
from src.cam_generator.cam_builder import CAMGenerator
from config import BRONZE_PATH, SILVER_PATH, GOLD_PATH

app = FastAPI(title="Credit Decisioning Engine API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_extractor = PDFExtractor()
feature_engineer = FeatureEngineer()
web_researcher = WebResearcher()
credit_model = CreditDecisionModel()
cam_generator = CAMGenerator()

# Load ML models
credit_model.load_models()

# Request/Response models
class CompanyInfo(BaseModel):
    company_name: str
    industry: str
    location: str
    established_year: Optional[int] = None
    registration_number: Optional[str] = None

class CreditCase(BaseModel):
    case_id: str
    company_info: CompanyInfo
    financial_data: Dict
    research_data: Dict
    ml_decision: Dict
    cam: Dict
    status: str

# In-memory storage (replace with database in production)
credit_cases = {}

@app.get("/")
async def root():
    return {"message": "Credit Decisioning Engine API"}

@app.post("/api/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    company_name: str = None,
    industry: str = None,
    location: str = None
):
    """Upload and process financial documents"""
    
    case_id = str(uuid.uuid4())
    
    # Save files to bronze layer
    bronze_case_path = BRONZE_PATH / case_id
    bronze_case_path.mkdir(exist_ok=True)
    
    extracted_data = {}
    
    for file in files:
        # Save file
        file_path = bronze_case_path / file.filename
        content = await file.read()
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Extract data from PDF
        if file.filename.endswith('.pdf'):
            pdf_data = pdf_extractor.extract_from_pdf(file_path)
            financial_values = pdf_extractor.extract_financial_values(pdf_data)
            extracted_data.update(financial_values)
    
    # Store in silver layer
    silver_case_path = SILVER_PATH / case_id
    silver_case_path.mkdir(exist_ok=True)
    
    with open(silver_case_path / 'financial_data.json', 'w') as f:
        json.dump(extracted_data, f)
    
    # Initialize case
    credit_cases[case_id] = CreditCase(
        case_id=case_id,
        company_info=CompanyInfo(
            company_name=company_name or "Unknown",
            industry=industry or "General",
            location=location or "Unknown"
        ),
        financial_data=extracted_data,
        research_data={},
        ml_decision={},
        cam={},
        status="uploaded"
    )
    
    return {
        "case_id": case_id,
        "status": "uploaded",
        "extracted_data": extracted_data
    }

@app.post("/api/process/{case_id}")
async def process_case(case_id: str):
    """Process uploaded documents through the pipeline"""
    
    if case_id not in credit_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = credit_cases[case_id]
    
    # Calculate financial ratios
    ratios = feature_engineer.calculate_financial_ratios(case.financial_data)
    
    # Generate risk signals
    signals = feature_engineer.generate_risk_signals(case.financial_data)
    
    # Update financial data
    case.financial_data.update(ratios)
    case.financial_data.update(signals)
    
    # Store in gold layer
    gold_case_path = GOLD_PATH / case_id
    gold_case_path.mkdir(exist_ok=True)
    
    with open(gold_case_path / 'features.json', 'w') as f:
        json.dump(case.financial_data, f)
    
    case.status = "processed"
    
    return {
        "case_id": case_id,
        "status": "processed",
        "features": case.financial_data
    }

@app.post("/api/research/{case_id}")
async def research_company(case_id: str):
    """Perform web research on the company"""
    
    if case_id not in credit_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = credit_cases[case_id]
    
    # Perform research
    research_results = web_researcher.research_company(
        case.company_info.company_name,
        case.company_info.industry
    )
    
    case.research_data = research_results
    case.status = "researched"
    
    return {
        "case_id": case_id,
        "status": "researched",
        "research_summary": research_results.get('summary', ''),
        "scores": research_results.get('scores', {})
    }

@app.post("/api/decision/{case_id}")
async def make_credit_decision(case_id: str):
    """Generate ML-based credit decision"""
    
    if case_id not in credit_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = credit_cases[case_id]
    
    # Combine all features
    all_features = {
        **case.financial_data,
        **case.research_data.get('scores', {})
    }
    
    # Create feature vector
    feature_vector = feature_engineer.create_feature_vector(
        case.financial_data,
        {k: v for k, v in case.financial_data.items() 
         if k in ['debt_to_equity', 'current_ratio', 'interest_coverage', 
                  'profit_margin', 'revenue_growth', 'cash_flow_ratio']},
        {k: v for k, v in case.financial_data.items()
         if k in ['legal_risk_flag', 'litigation_count', 'sector_risk_score']},
        case.research_data.get('scores', {})
    )
    
    # Make prediction
    ml_decision = credit_model.predict(feature_vector)
    
    case.ml_decision = ml_decision
    case.status = "decided"
    
    return {
        "case_id": case_id,
        "status": "decided",
        "decision": ml_decision
    }

@app.post("/api/cam/{case_id}")
async def generate_cam(case_id: str):
    """Generate Comprehensive Credit Appraisal Memo"""
    
    if case_id not in credit_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case = credit_cases[case_id]
    
    # Generate CAM
    cam = cam_generator.generate_cam(
        case.company_info.dict(),
        case.financial_data,
        case.research_data,
        case.ml_decision
    )
    
    case.cam = cam
    case.status = "completed"
    
    return {
        "case_id": case_id,
        "status": "completed",
        "cam": cam['full_document'],
        "decision": case.ml_decision
    }

@app.get("/api/case/{case_id}")
async def get_case(case_id: str):
    """Get complete case details"""
    
    if case_id not in credit_cases:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return credit_cases[case_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
