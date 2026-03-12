import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_LAKE_PATH = BASE_DIR / "data_lake"
BRONZE_PATH = DATA_LAKE_PATH / "bronze"
SILVER_PATH = DATA_LAKE_PATH / "silver"
GOLD_PATH = DATA_LAKE_PATH / "gold"

# Create directories
for path in [BRONZE_PATH, SILVER_PATH, GOLD_PATH]:
    path.mkdir(parents=True, exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Model parameters
MODEL_PATH = BASE_DIR / "models" / "credit_model.pkl"
FEATURE_COLUMNS = [
    'revenue', 'ebitda', 'total_assets', 'total_liabilities',
    'debt_to_equity', 'current_ratio', 'interest_coverage',
    'profit_margin', 'revenue_growth', 'cash_flow_ratio',
    'news_sentiment_score', 'reputation_score', 'industry_risk',
    'legal_risk_flag', 'sector_risk_score'
]

# Credit parameters
MIN_CREDIT_LIMIT = 100000
MAX_CREDIT_LIMIT = 10000000
BASE_INTEREST_RATE = 8.5
MAX_INTEREST_RATE = 18.0
