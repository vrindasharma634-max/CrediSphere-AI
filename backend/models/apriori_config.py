"""
Screen Configuration - Association Rule Mining (Apriori) or Collaborative Filtering
Recommends which widgets/screens should be shown to different user roles.
"""
import random

class AprioriWidgetRecommender:
    def __init__(self):
        self.algorithm = "Apriori_Association_Rules"
        
    def recommend_dashboard_layout(self, role):
        """
        Simulates recommending widgets based on what users of a similar role frequently use together.
        """
        widgets = []
        if role == "ADMIN":
            widgets = ["Demand Forecast Chart", "System Health", "Recent Approvals Table"]
        else:
            widgets = ["CrediScore Gauge", "Active Loan Progress", "Make a Payment Button"]
            
        # Simulate confidence scores
        recommendations = [{"widget": w, "confidence": round(random.uniform(0.7, 0.99), 2)} for w in widgets]
        
        return {
            "algorithm": self.algorithm,
            "role": role,
            "recommended_layout": recommendations
        }
