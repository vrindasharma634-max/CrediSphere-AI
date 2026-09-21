import random

def detect_signup_fraud(data):
    """
    Mock Isolation Forest implementation to detect anomalous signups.
    In production, this would load a trained sklearn IsolationForest model
    and predict based on features like IP, time of day, email domain, etc.
    """
    # Simple heuristic for demo: Block if email contains 'fraud'
    if 'fraud' in data.get('email', '').lower():
        return True
    
    # 2% chance of random anomaly detection for demo
    if random.random() < 0.02:
        return True
    return False

def detect_login_fraud(data):
    """
    Mock Isolation Forest implementation for login fraud.
    """
    # Block if too many attempts from same IP (simulated)
    if 'hacker' in data.get('email', '').lower():
        return True
    
    # 1% chance for demo
    if random.random() < 0.01:
        return True
    return False
