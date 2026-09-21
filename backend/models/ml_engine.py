import math

class CIBILSimulator:
    def __init__(self):
        self.model_name = "Dynamic_CIBIL_Estimator_v1"

    def calculate_score(self, income, employment_profile, existing_emi, requested_tenure_months):
        """
        Dynamically computes a simulated CIBIL score based on financial parameters.
        """
        income = max(1, float(income))
        existing_emi = max(0, float(existing_emi))
        requested_tenure_months = int(requested_tenure_months)

        # 1. Base Score derived logarithmically from income (higher income -> slightly higher base)
        # Assuming typical income 20k to 500k. Log base scales gracefully.
        base_score = 500 + (math.log10(income) - 4) * 80  
        base_score = max(400, min(800, base_score))

        # 2. Employment Profile Multipliers
        employment_multipliers = {
            'salaried_tier1': 1.10,     # Very stable
            'salaried': 1.05,
            'professional': 1.08,       # CA, Doctor
            'business': 1.00,
            'gig_worker': 0.90          # Less stable
        }
        multiplier = employment_multipliers.get(employment_profile, 1.0)
        
        # 3. Debt-to-Income (DTI) / FOIR Penalty
        dti = existing_emi / income
        
        dti_penalty = 0
        if dti > 0.60:
            dti_penalty = -150
        elif dti > 0.50:
            dti_penalty = -80
        elif dti > 0.40:
            dti_penalty = -40
        elif dti < 0.20:
            dti_penalty = +30  # Bonus for very low existing debt
            
        # Final Score Calculation
        final_score = (base_score * multiplier) + dti_penalty
        
        # Add a tiny bit of deterministic noise for "dynamic" feel
        noise = (income % 7) - 3 
        final_score = int(max(300, min(900, final_score + noise)))
        
        # 4. Loan Sanction Decisioning
        decision = self._generate_loan_terms(final_score, income, dti, requested_tenure_months)
        
        return {
            "score": final_score,
            "dti_percentage": round(dti * 100, 1),
            "decision": decision
        }

    def _generate_loan_terms(self, score, income, current_dti, tenure):
        # Strict FOIR limits
        if score < 640 or current_dti > 0.48:
            status = "High Risk"
            reason = "High DTI (exceeds 48%)" if current_dti > 0.48 else f"Subprime Credit Score ({score})"
            return {
                "status": "Rejected",
                "reason": reason,
                "max_sanction": 0,
                "interest_rate": "-",
                "max_emi": 0,
                "recommended_tenure": 0
            }
            
        elif score >= 720 and current_dti <= 0.35:
            status = "Prime"
            rate = 9.0  # Between 8.5% and 9.5%
            multiplier = 20
        else:
            status = "Review"
            rate = 11.5 # Between 10.5% and 12.5%
            multiplier = 10
            
        # Max allowable DTI for actual sanction sizing
        max_allowable_dti = 0.50 if status == "Prime" else 0.48
        available_dti = max(0, max_allowable_dti - current_dti)
        
        # Max monthly EMI they can afford right now
        max_affordable_emi = income * available_dti
            
        # Calculate theoretical max sanction based on multiplier and EMI affordability
        # PMT formula reversed to find PV (Present Value)
        # PV = EMI * (1 - (1 + r)^-n) / r
        monthly_rate = (rate / 100) / 12
        max_pv_by_emi = max_affordable_emi * (1 - math.pow(1 + monthly_rate, -tenure)) / monthly_rate
        
        max_pv_by_multiplier = income * multiplier
        
        # The final sanction is the minimum of what they can afford monthly vs flat multiplier limit
        final_sanction = min(max_pv_by_emi, max_pv_by_multiplier)
        
        return {
            "status": "Pre-Approved" if status == "Prime" else "Review",
            "band": status,
            "max_sanction": int(round(final_sanction, -3)), # Round to nearest 1000
            "interest_rate": rate,
            "max_emi": int(max_affordable_emi),
            "recommended_tenure": tenure
        }
