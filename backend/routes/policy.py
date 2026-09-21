"""
CrediSphere AI - Risk Policy Configuration Routes
Exposes Rule Engine, Bayesian Optimization Tuner, and Customer Cohort Simulator endpoints.
"""

from flask import Blueprint, jsonify, request
from extensions import db
from models.loan import Loan
from models.user import User
from models.bayesian_policy import RiskPolicyEngine, BayesianPolicyOptimizer

policy_bp = Blueprint('policy', __name__)
policy_engine = RiskPolicyEngine()
bayesian_tuner = BayesianPolicyOptimizer()

@policy_bp.route('/', methods=['GET'])
def get_policy():
    """
    Returns the complete risk policy configuration, sequential rules,
    score thresholds, escalation matrix, and live evaluation of registered customers.
    """
    try:
        data = policy_engine.get_policy_overview(
            db_session=db.session,
            LoanModel=Loan,
            UserModel=User
        )
        return jsonify({
            "status": "success",
            "data": data
        }), 200
    except Exception as e:
        print(f"Error in get_policy: {e}")
        data = policy_engine.get_policy_overview()
        return jsonify({
            "status": "success",
            "data": data,
            "warning": str(e)
        }), 200


@policy_bp.route('/update-config', methods=['POST'])
def update_policy_config():
    """
    Updates risk policy thresholds (e.g. minimum CrediScore, referral buffer, DTI cap).
    """
    try:
        payload = request.get_json() or {}
        updated = policy_engine.update_config(payload)
        
        # Re-evaluate registered customers with new parameters
        evals, summary = policy_engine.evaluate_registered_customers(
            db_session=db.session,
            LoanModel=Loan,
            UserModel=User
        )
        
        return jsonify({
            "status": "success",
            "message": "Risk policy thresholds updated successfully",
            "config": updated,
            "customer_evaluations": evals,
            "summary": summary
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@policy_bp.route('/toggle-rule', methods=['POST'])
def toggle_rule():
    """
    Toggles an individual decision rule between Active and Draft.
    """
    try:
        payload = request.get_json() or {}
        rule_id = payload.get('rule_id')
        enabled = payload.get('enabled', True)
        
        updated_rule = policy_engine.toggle_rule(rule_id, enabled)
        if not updated_rule:
            return jsonify({"status": "error", "message": f"Rule {rule_id} not found"}), 404
            
        evals, summary = policy_engine.evaluate_registered_customers(
            db_session=db.session,
            LoanModel=Loan,
            UserModel=User
        )
        
        return jsonify({
            "status": "success",
            "message": f"Rule {rule_id} status updated to {updated_rule['status']}",
            "rule": updated_rule,
            "customer_evaluations": evals,
            "summary": summary
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@policy_bp.route('/run-bayesian', methods=['POST'])
def run_bayesian_optimization():
    """
    Runs Bayesian Optimization with Gaussian Process surrogate model
    to recommend the optimal minimum credit score cutoff and risk thresholds.
    """
    try:
        payload = request.get_json() or {}
        target_npa = payload.get('target_default_rate_pct', 2.2)
        risk_appetite = payload.get('risk_appetite', 'MODERATE')
        
        optimization_result = bayesian_tuner.optimize(
            target_default_rate_pct=target_npa,
            risk_appetite=risk_appetite
        )
        
        return jsonify({
            "status": "success",
            "data": optimization_result
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@policy_bp.route('/save', methods=['POST'])
def save_policy():
    """
    Saves full risk policy changes and commits to audit log.
    """
    try:
        payload = request.get_json() or {}
        if 'config' in payload:
            policy_engine.update_config(payload['config'])
            
        return jsonify({
            "status": "success",
            "message": "All risk policy configuration changes committed successfully",
            "timestamp": policy_engine.config["last_updated"]
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
