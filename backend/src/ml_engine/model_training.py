import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))


import pandas as pd
import numpy as np
from pathlib import Path
from credit_model import CreditDecisionModel
from config import FEATURE_COLUMNS

def generate_synthetic_data(n=1000):
    data = []

    for _ in range(n):
        row = {
            'revenue': np.random.randint(1e6, 1e8),
            'ebitda': np.random.randint(1e5, 1e7),
            'total_assets': np.random.randint(1e6, 1e8),
            'total_liabilities': np.random.randint(1e5, 5e7),
            'debt_to_equity': np.random.uniform(0.1, 3),
            'current_ratio': np.random.uniform(0.5, 3),
            'interest_coverage': np.random.uniform(0.5, 10),
            'profit_margin': np.random.uniform(-0.1, 0.3),
            'revenue_growth': np.random.uniform(-0.1, 0.3),
            'cash_flow_ratio': np.random.uniform(0, 2),
            'news_sentiment_score': np.random.uniform(0, 1),
            'reputation_score': np.random.uniform(0, 1),
            'industry_risk': np.random.uniform(0, 1),
            'legal_risk_flag': np.random.randint(0, 2),
            'sector_risk_score': np.random.uniform(0, 1),
        }

        row['approved'] = 1 if row['profit_margin'] > 0 and row['debt_to_equity'] < 2 else 0
        row['credit_limit'] = np.random.randint(100000, 10000000)
        row['interest_rate'] = np.random.uniform(8.5, 18)

        data.append(row)

    return pd.DataFrame(data)

def train():
    print("Generating synthetic training data...")

    df = generate_synthetic_data()

    model = CreditDecisionModel()
    model.train_models(df)

    print("Training complete. Models saved.")

if __name__ == "__main__":
    train()
