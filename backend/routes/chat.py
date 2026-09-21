from flask import Blueprint, request, jsonify
import jwt
from config import Config
from models.user import User
import time
import random

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    """
    Live AI Chatbot endpoint for the customer portal.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized access'}), 401
    
    token = auth_header.split(" ")[1]
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']
    except Exception:
        return jsonify({'error': 'Invalid session'}), 401
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Extract user message
    request_data = request.json
    user_msg = request_data.get('message', '').lower()
    
    # Simulate AI processing delay
    time.sleep(1)
    
    # Basic simulated AI Logic
    first_name = user.name.split(" ")[0] if user.name else "there"
    
    if "loan" in user_msg and "apply" in user_msg:
        reply = f"Hi {first_name}! You can apply for a new loan directly from your dashboard. Based on your excellent CrediScore, you are pre-approved for up to ₹10,00,000. Would you like me to start the application?"
    elif "score" in user_msg or "credit" in user_msg:
        reply = f"Your current AI-generated CrediScore is excellent! Our XGBoost model indicates your consistent on-time payments have positively impacted your profile, {first_name}."
    elif "hello" in user_msg or "hi" in user_msg:
        reply = f"Hello {first_name}! I am your CrediSphere AI assistant. How can I help you with your finances today?"
    else:
        responses = [
            f"That's an interesting question, {first_name}. I can help you with loan applications, checking your credit score, or uploading KYC documents. What would you like to do?",
            f"I'm currently a prototype AI for CrediSphere. But I can tell you that your financial health looks great!",
            "I'm analyzing your profile now... Everything looks good. Is there anything specific about your loans you'd like to ask?"
        ]
        reply = random.choice(responses)
        
    return jsonify({
        "reply": reply,
        "model": "Llama-3-Fin-Tuned"
    }), 200
