from flask import Blueprint, request, jsonify
from models.ml_engine import CIBILSimulator

calculator_bp = Blueprint('calculator', __name__)

@calculator_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    
    # Extract inputs with defaults
    income = data.get('income', 0)
    employment_profile = data.get('employment_profile', 'salaried')
    existing_emi = data.get('existing_emi', 0)
    requested_tenure_months = data.get('requested_tenure_months', 36)
    
    if income <= 0:
        return jsonify({
            "score": 300,
            "dti_percentage": 0,
            "decision": {
                "status": "Awaiting Input",
                "max_sanction": 0,
                "interest_rate": "-",
                "max_emi": 0,
                "recommended_tenure": requested_tenure_months
            }
        })

    # Run ML simulation
    engine = CIBILSimulator()
    result = engine.calculate_score(income, employment_profile, existing_emi, requested_tenure_months)
    
    return jsonify(result), 200
