import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
import xgboost as xgb
import shap
from typing import Dict, Tuple
from config import MODEL_PATH, FEATURE_COLUMNS

class CreditDecisionModel:
    """Machine Learning model for credit decisions"""
    
    def __init__(self):
        self.approval_model = None
        self.limit_model = None
        self.rate_model = None
        self.feature_columns = FEATURE_COLUMNS
        self.explainer = None
        
    def train_models(self, training_data: pd.DataFrame):
        """Train all credit decision models"""
        
        # Prepare features
        X = training_data[self.feature_columns]
        
        # Train approval model (binary classification)
        y_approval = training_data['approved']
        self.approval_model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
        self.approval_model.fit(X, y_approval)
        
        # Train credit limit model (regression)
        approved_data = training_data[training_data['approved'] == 1]
        X_approved = approved_data[self.feature_columns]
        y_limit = approved_data['credit_limit']
        
        self.limit_model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42
        )
        self.limit_model.fit(X_approved, y_limit)
        
        # Train interest rate model (regression)
        y_rate = approved_data['interest_rate']
        self.rate_model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.1,
            random_state=42
        )
        self.rate_model.fit(X_approved, y_rate)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.approval_model)
        
        # Save models
        self.save_models()
    
    def predict(self, features: pd.DataFrame) -> Dict:
        """Make credit decision predictions"""
        
        # Ensure correct feature order
        features = features[self.feature_columns]
        
        # Predict approval probability
        approval_prob = self.approval_model.predict_proba(features)[0, 1]
        approved = approval_prob > 0.5
        
        # Calculate risk score (inverse of approval probability)
        risk_score = 1 - approval_prob
        
        # Predict credit limit and interest rate if approved
        if approved:
            credit_limit = self.limit_model.predict(features)[0]
            interest_rate = self.rate_model.predict(features)[0]
            
            # Apply bounds
            credit_limit = np.clip(credit_limit, 100000, 10000000)
            interest_rate = np.clip(interest_rate, 8.5, 18.0)
        else:
            credit_limit = 0
            interest_rate = 0
        
        # Get SHAP values for explainability
        shap_values = self.explainer.shap_values(features)
        
        # Get top factors
        feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': np.abs(shap_values[0])
        }).sort_values('importance', ascending=False)
        
        top_factors = feature_importance.head(5).to_dict('records')
        
        return {
            'approved': approved,
            'approval_probability': float(approval_prob),
            'risk_score': float(risk_score),
            'credit_limit': float(credit_limit),
            'interest_rate': float(interest_rate),
            'risk_grade': self._calculate_risk_grade(risk_score),
            'top_factors': top_factors
        }
    
    def _calculate_risk_grade(self, risk_score: float) -> str:
        """Calculate risk grade from score"""
        
        if risk_score < 0.2:
            return 'A'
        elif risk_score < 0.4:
            return 'B'
        elif risk_score < 0.6:
            return 'C'
        elif risk_score < 0.8:
            return 'D'
        else:
            return 'E'
    
    def save_models(self):
        """Save trained models to disk"""
        
        models = {
            'approval_model': self.approval_model,
            'limit_model': self.limit_model,
            'rate_model': self.rate_model
        }
        
        MODEL_PATH.parent.mkdir(exist_ok=True)
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(models, f)
    
    def load_models(self):
        """Load trained models from disk"""
        
        try:
            with open(MODEL_PATH, 'rb') as f:
                models = pickle.load(f)
                
            self.approval_model = models['approval_model']
            self.limit_model = models['limit_model']
            self.rate_model = models['rate_model']
            
            # Reinitialize explainer
            self.explainer = shap.TreeExplainer(self.approval_model)
            
            return True
        except FileNotFoundError:
            print("No saved models found. Please train models first.")
            return False
