import pandas as pd
import numpy as np
from typing import Dict

class FeatureEngineer:
    """Generate ML features from financial data"""
    
    def calculate_financial_ratios(self, financial_data: Dict) -> Dict:
        """Calculate key financial ratios"""
        
        ratios = {}
        
        # Debt to Equity
        if 'total_liabilities' in financial_data and 'equity' in financial_data:
            if financial_data['equity'] > 0:
                ratios['debt_to_equity'] = financial_data['total_liabilities'] / financial_data['equity']
            else:
                ratios['debt_to_equity'] = np.inf
        else:
            ratios['debt_to_equity'] = 0
        
        # Current Ratio
        if 'current_assets' in financial_data and 'current_liabilities' in financial_data:
            if financial_data['current_liabilities'] > 0:
                ratios['current_ratio'] = financial_data['current_assets'] / financial_data['current_liabilities']
            else:
                ratios['current_ratio'] = np.inf
        else:
            ratios['current_ratio'] = 1.0
        
        # Interest Coverage
        if 'ebitda' in financial_data and 'interest_expense' in financial_data:
            if financial_data.get('interest_expense', 0) > 0:
                ratios['interest_coverage'] = financial_data['ebitda'] / financial_data['interest_expense']
            else:
                ratios['interest_coverage'] = np.inf
        else:
            ratios['interest_coverage'] = 2.0
        
        # Profit Margin
        if 'profit' in financial_data and 'revenue' in financial_data:
            if financial_data['revenue'] > 0:
                ratios['profit_margin'] = financial_data['profit'] / financial_data['revenue']
            else:
                ratios['profit_margin'] = 0
        else:
            ratios['profit_margin'] = 0.1
        
        # Revenue Growth (placeholder - would need historical data)
        ratios['revenue_growth'] = 0.15  # Default 15% growth
        
        # Cash Flow Ratio
        if 'cash_flow' in financial_data and 'current_liabilities' in financial_data:
            if financial_data['current_liabilities'] > 0:
                ratios['cash_flow_ratio'] = financial_data['cash_flow'] / financial_data['current_liabilities']
            else:
                ratios['cash_flow_ratio'] = 1.0
        else:
            ratios['cash_flow_ratio'] = 0.5
        
        return ratios
    
    def generate_risk_signals(self, financial_data: Dict, research_data: Dict = None) -> Dict:
        """Generate risk signal features"""
        
        signals = {}
        
        # Legal risk flag (from research or default)
        signals['legal_risk_flag'] = research_data.get('legal_issues', 0) if research_data else 0
        
        # Litigation count
        signals['litigation_count'] = research_data.get('litigation_count', 0) if research_data else 0
        
        # Sector risk score (industry-specific)
        industry = research_data.get('industry', 'general') if research_data else 'general'
        sector_risks = {
            'technology': 0.3,
            'finance': 0.2,
            'manufacturing': 0.5,
            'retail': 0.6,
            'general': 0.4
        }
        signals['sector_risk_score'] = sector_risks.get(industry.lower(), 0.4)
        
        return signals
    
    def create_feature_vector(self, financial_data: Dict, ratios: Dict, 
                            signals: Dict, research_scores: Dict) -> pd.DataFrame:
        """Create final feature vector for ML model"""
        
        features = {
            'revenue': financial_data.get('revenue', 0),
            'ebitda': financial_data.get('ebitda', 0),
            'total_assets': financial_data.get('total_assets', 0),
            'total_liabilities': financial_data.get('total_liabilities', 0),
            **ratios,
            **signals,
            **research_scores
        }
        
        # Ensure all required features are present
        for col in ['news_sentiment_score', 'reputation_score', 'industry_risk']:
            if col not in features:
                features[col] = 0.5  # Default neutral score
        
        return pd.DataFrame([features])
