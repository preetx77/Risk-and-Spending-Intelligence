# PREET SONAR 
# PRN : 20240802258

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple

class TransactionAnomalyDetector:
    
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        
    def engineer_features(self, df):
        """Create features from transactions"""
        features = df.copy()
        features['timestamp'] = pd.to_datetime(features['Date'])
        
        # Time features
        features['hour'] = features['timestamp'].dt.hour
        features['day_of_week'] = features['timestamp'].dt.dayofweek
        features['is_weekend'] = (features['day_of_week'] >= 5).astype(int)
        
        # Amount features
        features['amount_log'] = np.log1p(features['Amount'])
        category_stats = df.groupby('Category')['Amount'].agg(['mean', 'std'])
        features = features.merge(category_stats, left_on='Category', right_index=True)
        features['amount_z_score'] = (features['Amount'] - features['mean']) / (features['std'] + 0.01)
        
        # Merchant features
        merchant_freq = df['Merchant'].value_counts()
        features['merchant_frequency'] = features['Merchant'].map(merchant_freq)
        features['is_new_merchant'] = (features['merchant_frequency'] == 1).astype(int)
        
        return features
    
    def fit(self, transactions_df):
        """Train the detector"""
        features_df = self.engineer_features(transactions_df)
        X = features_df[['amount_log', 'hour', 'day_of_week', 'amount_z_score', 
                        'merchant_frequency', 'is_new_merchant']].fillna(0)
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X))
        return self
    
    def predict(self, transactions_df):
        """Detect anomalies"""
        features_df = self.engineer_features(transactions_df)
        X = features_df[['amount_log', 'hour', 'day_of_week', 'amount_z_score',
                        'merchant_frequency', 'is_new_merchant']].fillna(0)
        predictions = self.model.predict(self.scaler.transform(X))
        scores = self.model.score_samples(self.scaler.transform(X))
        risk_scores = 1 - ((scores - scores.min()) / (scores.max() - scores.min() + 1e-10))
        return predictions, risk_scores
    
    def explain(self, transaction, features):
        """Explain why flagged"""
        reasons = []
        if features['amount_z_score'] > 2:
            reasons.append(f"{features['amount_z_score']:.1f}x above typical spending")
        if features['hour'] < 6 or features['hour'] > 23:
            reasons.append(f"Unusual time ({int(features['hour'])}:00)")
        if features['is_new_merchant'] == 1:
            reasons.append("New merchant")
        return reasons or ["Pattern deviation"]
    
    def analyze(self, transactions_df, threshold=0.7):
        """Full analysis with explanations"""
        features_df = self.engineer_features(transactions_df)
        predictions, risk_scores = self.predict(transactions_df)
        
        result = transactions_df.copy()
        result['risk_score'] = risk_scores
        result['risk_level'] = pd.cut(risk_scores, bins=[0, 0.3, 0.7, 1.0],
                                      labels=['Low', 'Medium', 'High'])
        
        result['explanation'] = None
        for idx in result[risk_scores >= threshold].index:
            reasons = self.explain(result.loc[idx], features_df.loc[idx])
            result.at[idx, 'explanation'] = ' | '.join(reasons)
        
        return result

# Usage example
if __name__ == "__main__":
    # Load your data
    df = pd.read_csv('data/raw/comprehensive_student_finance_enhanced.csv')
    
    # Train
    detector = TransactionAnomalyDetector()
    detector.fit(df)
    
    # Detect anomalies
    results = detector.analyze(df)
    anomalies = results[results['risk_level'] == 'High']
    
    print(f"Detected {len(anomalies)} high-risk transactions")
    for _, row in anomalies.iterrows():
        print(f"${row['Amount']:.2f} at {row['Merchant']} - Risk: {row['risk_score']:.2f}")
        print(f"  {row['explanation']}\n")