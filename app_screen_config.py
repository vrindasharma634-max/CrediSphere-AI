"""
CrediSphere AI - Customer Screen Configuration & Dynamic Portal Personalization
Unified Flask REST API with Association Rule Mining (Apriori Engine)
and Item-Based Collaborative Filtering Engine.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from backend.app_screen_config import create_app, screen_config_bp, ml_engine

app = create_app()

if __name__ == '__main__':
    print("Starting CrediSphere Screen Config & Apriori Recommendation Engine...")
    app.run(host='0.0.0.0', port=5005, debug=True)
