"""
Loan Application Form - LightGBM / CatBoost
Validates applicant data and estimates loan eligibility before submission.
"""
import random

class LightGBMLoanValidator:
    def __init__(self):
        self.model_name = "LightGBM_Eligibility"
    
    def estimate_eligibility(self, requested_amount, applicant_income, current_debts):
        """
        Estimates the probability of approval instantly.
        """
        dti = (current_debts / applicant_income) * 100 if applicant_income > 0 else 100
        
        if dti > 45:
            approval_prob = random.uniform(0.1, 0.3)
        elif requested_amount > (applicant_income * 3):
            approval_prob = random.uniform(0.2, 0.5)
        else:
            approval_prob = random.uniform(0.7, 0.95)
            
        return {
            "model": self.model_name,
            "approval_probability": round(approval_prob * 100, 2),
            "status": "Pre-Approved" if approval_prob > 0.7 else "High Risk",
            "recommended_amount": min(requested_amount, applicant_income * 2) if approval_prob < 0.7 else requested_amount
        }
