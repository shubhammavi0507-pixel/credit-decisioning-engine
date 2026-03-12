import pdfplumber
import pandas as pd
import re
from typing import Dict, List, Any
from pathlib import Path
import json

class PDFExtractor:
    """Extract financial data from PDF documents"""
    
    def __init__(self):
        self.financial_keywords = [
            'revenue', 'sales', 'income', 'ebitda', 'profit',
            'assets', 'liabilities', 'equity', 'debt', 'cash flow',
            'current assets', 'current liabilities'
        ]
        
    def extract_from_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract text and tables from PDF"""
        extracted_data = {
            'text': [],
            'tables': [],
            'metadata': {}
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                extracted_data['metadata'] = {
                    'num_pages': len(pdf.pages),
                    'filename': pdf_path.name
                }
                
                for page_num, page in enumerate(pdf.pages):
                    # Extract text
                    text = page.extract_text()
                    if text:
                        extracted_data['text'].append({
                            'page': page_num + 1,
                            'content': text
                        })
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            extracted_data['tables'].append({
                                'page': page_num + 1,
                                'data': table
                            })
                            
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            
        return extracted_data
    
    def extract_financial_values(self, extracted_data: Dict) -> Dict[str, float]:
        """Extract specific financial values from text and tables"""
        financial_data = {}
        
        # Process text
        full_text = ' '.join([page['content'] for page in extracted_data['text']])
        
        # Pattern to find numbers with financial keywords
        for keyword in self.financial_keywords:
            pattern = rf'{keyword}[:\s]*[\$₹]?\s*([\d,]+\.?\d*)\s*(million|billion|cr|lakh)?'
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            
            if matches:
                value = self._parse_number(matches[0])
                financial_data[keyword.replace(' ', '_')] = value
        
        # Process tables
        for table_data in extracted_data['tables']:
            df = pd.DataFrame(table_data['data'])
            
            # Try to identify financial statement structure
            if len(df.columns) >= 2:
                for idx, row in df.iterrows():
                    for keyword in self.financial_keywords:
                        if isinstance(row[0], str) and keyword in row[0].lower():
                            try:
                                value = self._parse_number(row[1])
                                if value:
                                    financial_data[keyword.replace(' ', '_')] = value
                            except:
                                continue
                                
        return financial_data
    
    def _parse_number(self, value) -> float:
        """Parse string number to float"""
        if isinstance(value, (int, float)):
            return float(value)
        
        if isinstance(value, tuple):
            value = value[0]
            
        if isinstance(value, str):
            # Remove currency symbols and commas
            value = re.sub(r'[₹$,]', '', value)
            
            try:
                num = float(value)
                
                # Handle multipliers
                if 'million' in str(value).lower():
                    num *= 1000000
                elif 'billion' in str(value).lower():
                    num *= 1000000000
                elif 'cr' in str(value).lower():
                    num *= 10000000
                elif 'lakh' in str(value).lower():
                    num *= 100000
                    
                return num
            except:
                return 0.0
        
        return 0.0
