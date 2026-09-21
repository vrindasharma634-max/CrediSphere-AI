"""
Login/Signup - Isolation Forest
Detects anomalous login locations or rapid successive signups.
"""
import random

class IsolationForestFraudDetector:
    def __init__(self):
        self.model_name = "IsolationForest"
        self.contamination = 0.05
        self.is_trained = True

    def predict_fraud(self, user_ip, login_time, user_agent):
        """
        Simulates an anomaly detection score.
        Returns a dict with 'is_fraud' boolean and 'anomaly_score'.
        """
        # Simulation logic
        anomaly_score = random.uniform(0.1, 0.9) # Safe score by default for demo
        # Occasionally simulate anomaly
        if random.random() < 0.05:
            anomaly_score = -0.1
            
        # Scores < 0 are considered anomalies in sklearn's Isolation Forest
        is_fraud = anomaly_score < 0
        
        return {
            "model": self.model_name,
            "anomaly_score": round(anomaly_score, 4),
            "is_fraud": is_fraud,
            "action": "block_user" if is_fraud else "allow_login"
        }
