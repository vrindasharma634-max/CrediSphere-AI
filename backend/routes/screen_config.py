"""
CrediSphere AI - Screen Configuration Routes
Imports and exposes the unified Screen Config & Apriori Recommendation Engine.
"""

from app_screen_config import screen_config_bp

# Export screen_config_bp so app.py picks it up directly
__all__ = ['screen_config_bp']
