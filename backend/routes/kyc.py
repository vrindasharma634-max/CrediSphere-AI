from flask import Blueprint, jsonify
kyc_bp = Blueprint('kyc', __name__)
@kyc_bp.route('/upload', methods=['POST'])
def upload():
    return jsonify({'message': 'KYC uploaded'}), 200
