from flask import Blueprint, jsonify
credit_bp = Blueprint('credit', __name__)
@credit_bp.route('/intelligence', methods=['GET'])
def intelligence():
    return jsonify({'message': 'Credit intelligence data'}), 200
