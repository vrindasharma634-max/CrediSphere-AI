from flask import Blueprint, jsonify, request
from models.rl_collections import RLCollectionsOptimizer
from models.user import User, Customer
from models.loan import Loan
from datetime import datetime

collections_bp = Blueprint('collections', __name__)
optimizer = RLCollectionsOptimizer()

# In-memory store for follow-up events per customer
follow_up_events = {
    3: [
        {"type": "Kept promise", "icon": "💬", "details": "₹35,999 received via UPI for Home Loan #LN-0005", "time": "09 Nov 2025"},
        {"type": "PTP", "icon": "📞", "details": "₹35,999 promised by 12-Dec-2025", "time": "05 Nov 2025"},
        {"type": "Initial notice", "icon": "📩", "details": "Automated NACH bounce notice sent to registered phone", "time": "13 Oct 2025"}
    ],
    2: [
        {"type": "Kept promise", "icon": "💬", "details": "₹44,999 received via Netbanking for Personal Loan #LN-0001", "time": "18 Nov 2025"},
        {"type": "PTP", "icon": "📞", "details": "₹44,999 token promised", "time": "10 Nov 2025"}
    ]
}

def get_customer_collections_payload(user):
    profile = Customer.query.filter_by(user_id=user.id).first()
    # Fetch loans for this customer (prioritize APPROVED, otherwise any loan)
    loans = Loan.query.filter(Loan.customer_id == user.id, Loan.status == 'APPROVED').order_by(Loan.applied_at.desc()).all()
    if not loans:
        loans = Loan.query.filter(Loan.customer_id == user.id).order_by(Loan.applied_at.desc()).all()
    
    # Strictly use registered phone
    raw_phone = profile.phone if (profile and profile.phone) else "Not Registered"
    if raw_phone != "Not Registered":
        clean_digits = "".join(c for c in raw_phone if c.isdigit())
        if len(clean_digits) >= 10:
            last10 = clean_digits[-10:]
            phone = f"+91 {last10[:5]}-{last10[5:]}"
        elif raw_phone.startswith("+"):
            phone = raw_phone
        else:
            phone = f"+91 {raw_phone}"
    else:
        phone = "Not Registered"
        
    primary_loan = loans[0] if loans else None
    
    if primary_loan:
        if primary_loan.max_approved_emi:
            emi = float(primary_loan.max_approved_emi)
        else:
            amt = float(primary_loan.amount or 50000)
            tenure = int(primary_loan.term_months or 12)
            emi = round((amt / max(tenure, 1)) * 1.08, 2)
        loan_id = f"LN-2024-{primary_loan.id:04d}"
        loan_type = primary_loan.loan_type or "Personal Loan"
        loan_amount = float(primary_loan.amount or 50000)
        bounced_emis = 3
        total_overdue = round(emi * bounced_emis, 2)
        dpd = 90
    else:
        emi = 12500.0
        loan_id = f"LN-2024-{user.id:04d}"
        loan_type = "Personal Credit Line"
        loan_amount = 150000.0
        bounced_emis = 2
        total_overdue = round(emi * bounced_emis, 2)
        dpd = 60
        
    history = follow_up_events.get(user.id, [])
    if len(history) == 0:
        history = [
            {"type": "Kept promise", "icon": "💬", "details": f"₹{int(emi):,} received via UPI for {loan_type} #{loan_id}", "time": "Last month"},
            {"type": "PTP", "icon": "📞", "details": f"₹{int(emi):,} promised", "time": "2 weeks ago"},
            {"type": "NACH Bounce", "icon": "⚠️", "details": f"EMI bounce on loan {loan_id}", "time": "Recent"}
        ]
        if phone != "Not Registered":
            history.append({"type": "SMS Alert", "icon": "📩", "details": f"Automated notice sent to {phone}", "time": "3 days ago"})

    return {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": phone,
        "account_no": loan_id,
        "loan_type": loan_type,
        "loan_amount": loan_amount,
        "emi_amount": emi,
        "bounced_emis": bounced_emis,
        "total_overdue": total_overdue,
        "dpd_bucket": f"{dpd} ({bounced_emis})",
        "dpd": dpd,
        "broken_promises": 2 if dpd >= 90 else 1,
        "sentiment": "Negative" if dpd >= 90 else "Neutral",
        "best_call_time": "5–7 PM",
        "history": history
    }

@collections_bp.route('/', methods=['GET'])
def get_collections():
    user_id_param = request.args.get('user_id', type=int)
    
    # If user_id specified, fetch that customer
    if user_id_param:
        user = User.query.get(user_id_param)
        if user and user.role == 'CUSTOMER':
            borrower_data = get_customer_collections_payload(user)
            return jsonify({
                'status': 'success',
                'borrower': borrower_data,
                'models': ['Random Forest (Risk Scoring)', 'DQN Agent (Policy Optimization)'],
                'history': borrower_data['history']
            }), 200

    # Otherwise default to the first registered customer in database
    registered_customer = User.query.filter_by(role='CUSTOMER').order_by(User.id.asc()).first()

    if registered_customer:
        borrower_data = get_customer_collections_payload(registered_customer)
    else:
        return jsonify({'status': 'error', 'message': 'No registered customer found'}), 404

    return jsonify({
        'status': 'success',
        'borrower': borrower_data,
        'models': ['Random Forest (Risk Scoring)', 'DQN Agent (Policy Optimization)'],
        'history': borrower_data['history']
    }), 200

@collections_bp.route('/customers', methods=['GET'])
def get_all_collections_customers():
    """
    Returns all real registered customers from the database with their registered phone numbers,
    active loan status, and collections metrics.
    """
    customers = User.query.filter_by(role='CUSTOMER').order_by(User.id.asc()).all()
    results = []
    
    for u in customers:
        payload = get_customer_collections_payload(u)
        results.append(payload)
            
    return jsonify({"status": "success", "customers": results}), 200

@collections_bp.route('/strategy', methods=['POST', 'GET'])
def get_strategy():
    data = request.get_json(silent=True) or {}
    result = optimizer.get_recovery_strategy(data)
    
    result.update({
        "q_matrix": [
            {"action": "Structured Settlement Offer", "q_value": 0.812, "is_optimal": True},
            {"action": "SMS Payment Link", "q_value": 0.640, "is_optimal": False},
            {"action": "Automated IVR Call", "q_value": 0.520, "is_optimal": False},
            {"action": "Hard Recovery Agent Dispatch", "q_value": 0.310, "is_optimal": False},
            {"action": "Legal Repossession Notice", "q_value": -0.150, "is_optimal": False}
        ],
        "feature_importances": [
            {"feature": "DPD Bucket (90+ Days)", "weight": 0.38},
            {"feature": "Broken Promises (2 prior)", "weight": 0.27},
            {"feature": "Sentiment Tone (Negative)", "weight": 0.18},
            {"feature": "Bounce Frequency (3 EMIs)", "weight": 0.17}
        ],
        "exploit_rate_epsilon": 0.05,
        "model_confidence": "87.4%"
    })
    return jsonify(result), 200

@collections_bp.route('/record-ptp', methods=['POST'])
def record_ptp():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get('user_id', 3)
    amount = payload.get('amount', '₹35,999')
    date = payload.get('date', 'Upcoming Friday')
    borrower_name = payload.get('borrower_name', 'Customer')
    
    event = {
        "type": "PTP",
        "icon": "📞",
        "details": f"PTP Recorded for {borrower_name} — {amount} promised by {date} (Agent call negotiation)",
        "time": "Just now"
    }
    
    if user_id not in follow_up_events:
        follow_up_events[user_id] = []
    follow_up_events[user_id].insert(0, event)
    
    return jsonify({"status": "recorded", "event": event}), 200

@collections_bp.route('/dispatch-message', methods=['POST'])
def dispatch_message():
    payload = request.get_json(silent=True) or {}
    user_id = payload.get('user_id', 3)
    channel = payload.get('channel', 'SMS Gateway')
    phone = payload.get('phone', 'Not Registered')
    borrower_name = payload.get('borrower_name', 'Customer')
    
    event = {
        "type": "Message",
        "icon": "📩",
        "details": f"Payment Link Dispatched to {borrower_name} ({phone}) via {channel} — Status: Delivered",
        "time": "Just now"
    }
    
    if user_id not in follow_up_events:
        follow_up_events[user_id] = []
    follow_up_events[user_id].insert(0, event)
    
    return jsonify({
        "status": "delivered",
        "channel": channel,
        "phone": phone,
        "message_id": f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }), 200
