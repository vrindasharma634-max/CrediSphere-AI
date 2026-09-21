from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy
import sys
import os

# Ensure backend directory is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)

    # Register blueprints (routes)
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.customer import customer_bp
    from routes.loan import loan_bp
    from routes.credit import credit_bp
    from routes.kyc import kyc_bp
    from routes.collections import collections_bp
    from routes.reports import reports_bp
    from routes.policy import policy_bp
    from routes.screen_config import screen_config_bp
    from routes.chat import chat_bp
    from routes.calculator import calculator_bp
    from routes.document import document_bp
    from routes.legal import legal_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(loan_bp, url_prefix='/api/loans')
    app.register_blueprint(credit_bp, url_prefix='/api/credit')
    app.register_blueprint(kyc_bp, url_prefix='/api/kyc')
    app.register_blueprint(collections_bp, url_prefix='/api/collections')
    app.register_blueprint(legal_bp, url_prefix='/api/legal')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(policy_bp, url_prefix='/api/risk-policy')
    app.register_blueprint(screen_config_bp, url_prefix='/api/screen-config')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(calculator_bp, url_prefix='/api/calculator')
    app.register_blueprint(document_bp, url_prefix='/api/documents')

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy", "service": "CrediSphere AI"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5004)
