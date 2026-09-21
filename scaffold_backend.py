import os

base_path = "backend/routes"
files = {
    "customer.py": """from flask import Blueprint, jsonify\ncustomer_bp = Blueprint('customer', __name__)\n@customer_bp.route('/dashboard', methods=['GET'])\ndef dashboard():\n    return jsonify({'message': 'Customer dashboard data'}), 200\n""",
    "loan.py": """from flask import Blueprint, jsonify\nloan_bp = Blueprint('loan', __name__)\n@loan_bp.route('/apply', methods=['POST'])\ndef apply():\n    return jsonify({'message': 'Loan application submitted'}), 201\n""",
    "credit.py": """from flask import Blueprint, jsonify\ncredit_bp = Blueprint('credit', __name__)\n@credit_bp.route('/intelligence', methods=['GET'])\ndef intelligence():\n    return jsonify({'message': 'Credit intelligence data'}), 200\n""",
    "kyc.py": """from flask import Blueprint, jsonify\nkyc_bp = Blueprint('kyc', __name__)\n@kyc_bp.route('/upload', methods=['POST'])\ndef upload():\n    return jsonify({'message': 'KYC uploaded'}), 200\n""",
    "collections.py": """from flask import Blueprint, jsonify\ncollections_bp = Blueprint('collections', __name__)\n@collections_bp.route('/', methods=['GET'])\ndef get_collections():\n    return jsonify({'message': 'Collections data'}), 200\n""",
    "reports.py": """from flask import Blueprint, jsonify\nreports_bp = Blueprint('reports', __name__)\n@reports_bp.route('/', methods=['GET'])\ndef get_reports():\n    return jsonify({'message': 'Reports data'}), 200\n""",
    "policy.py": """from flask import Blueprint, jsonify\npolicy_bp = Blueprint('policy', __name__)\n@policy_bp.route('/', methods=['GET'])\ndef get_policy():\n    return jsonify({'message': 'Policy data'}), 200\n""",
    "screen_config.py": """from flask import Blueprint, jsonify\nscreen_config_bp = Blueprint('screen_config', __name__)\n@screen_config_bp.route('/', methods=['GET'])\ndef get_config():\n    return jsonify({'message': 'Screen config'}), 200\n"""
}

for filename, content in files.items():
    with open(os.path.join(base_path, filename), "w") as f:
        f.write(content)

print("Scaffolded backend routes")
