from flask import Blueprint, request, jsonify
import jwt
from config import Config
from extensions import db
from models.user import User
from models.loan import Loan
from models.ml_engine import CIBILSimulator

loan_bp = Blueprint('loan', __name__)

@loan_bp.route('/apply', methods=['POST'])
def apply():
    """
    Process new loan application, run AI pre-check, and save to database.
    """
    # 1. Authenticate User
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

    # 2. Parse Application Data
    payload = request.json
    income = float(payload.get('income', 0))
    employment_profile = payload.get('employment_type', 'salaried')
    existing_emi = float(payload.get('existing_emi', 0))
    tenure = int(payload.get('term_months', 36))
    requested_amount = float(payload.get('amount', 0))

    # 3. Run AI Simulation
    engine = CIBILSimulator()
    ai_result = engine.calculate_score(income, employment_profile, existing_emi, tenure)
    
    decision = ai_result['decision']
    is_approved = decision.get('status') == 'Pre-Approved'

    # Standard bank EMI formula
    raw_rate = decision.get('interest_rate')
    try:
        rate = float(raw_rate) if raw_rate and str(raw_rate).strip() != '-' else 10.5
    except (ValueError, TypeError):
        rate = 10.5

    r_monthly = (rate / 100.0) / 12.0
    if tenure > 0 and requested_amount > 0:
        emi_calc = round((requested_amount * r_monthly * ((1 + r_monthly) ** tenure)) / (((1 + r_monthly) ** tenure) - 1), 2)
    else:
        emi_calc = round(requested_amount * 0.032, 2)

    # All newly submitted applications start as PENDING awaiting admin approval
    final_status = 'PENDING'

    from models.user import Customer
    cust = Customer.query.filter_by(user_id=user.id).first()

    # Extract PAN & Aadhaar (from payload or fallback to customer profile)
    pan_num = payload.get('pan_number') or (cust.pan_number if cust else None) or f"PAN{user.id:04d}K"
    aadhaar_num = payload.get('aadhaar_number') or (cust.aadhaar_number if cust else None) or f"8899 {user.id:04d} 4455"
    id_doc = payload.get('id_document_name') or f"id_proof_pan_aadhaar_{user.id}.pdf"
    income_doc = payload.get('income_document_name') or f"income_statement_3m_{user.id}.pdf"

    # 4. Save to Database
    new_loan = Loan(
        customer_id=user.id,
        loan_type=payload.get('loan_type', 'Personal Loan'),
        amount=requested_amount,
        purpose=payload.get('purpose', 'Personal / General Purpose'),
        term_months=tenure,
        income=income,
        employment_type=employment_profile,
        existing_emi=existing_emi,
        pan_number=pan_num,
        aadhaar_number=aadhaar_num,
        id_document_name=id_doc,
        income_document_name=income_doc,
        status=final_status,
        ai_score=ai_result['score'],
        interest_rate=rate,
        max_approved_emi=emi_calc,
        repaid_emis=0,
        outstanding_balance=requested_amount
    )
    
    # Update customer profile with PAN, Aadhaar and income if provided
    if cust:
        if income > 0:
            cust.annual_income = income
        if pan_num and not cust.pan_number:
            cust.pan_number = pan_num
        if aadhaar_num and not cust.aadhaar_number:
            cust.aadhaar_number = aadhaar_num
        
    db.session.add(new_loan)
    db.session.commit()

    loan_acct = f"LAN-2024-{user.id:04d}-{new_loan.id:02d}"
    direct_pay_link = f"http://localhost:5500/pages/customer-dashboard.html?pay_loan={new_loan.id}&inst=1&amount={round(emi_calc)}"
    
    # Dispatch Real SMS if Approved
    if decision['status'] == 'Pre-Approved':
        phone = user.customer_profile.phone if user.customer_profile else None
        sms_msg = f"Your CrediSphere loan for Rs.{requested_amount} is approved! Max Sanction: Rs.{decision['max_sanction']}."
        
        print("\n" + "="*60)
        if phone:
            print(f"📨 DISPATCHING REAL SMS TO: {phone}")
            try:
                import requests
                resp = requests.post('https://textbelt.com/text', {
                    'phone': phone,
                    'message': sms_msg,
                    'key': 'textbelt',
                })
                result = resp.json()
                print("TEXTBELT RESPONSE:", result)
                if not result.get('success'):
                    decision['sms_error'] = result.get('error', 'Unknown SMS Gateway Error')
                    decision['sms_sent'] = False
                else:
                    decision['sms_sent'] = True
            except Exception as e:
                print("SMS API ERROR:", e)
                decision['sms_error'] = str(e)
                decision['sms_sent'] = False
        else:
            print("📨 NO PHONE NUMBER FOUND FOR SMS")
            decision['sms_error'] = "No phone number registered"
            decision['sms_sent'] = False
        print("="*60 + "\n")
        
    else:
        decision['sms_sent'] = False

    return jsonify({
        'message': 'Loan application successfully processed',
        'loan_id': new_loan.id,
        'loan_account_no': loan_acct,
        'status': final_status,
        'sanctioned_amount': requested_amount,
        'emi': emi_calc,
        'interest_rate': rate,
        'term_months': tenure,
        'first_due_date': '05 Oct 2026',
        'payment_link': direct_pay_link,
        'ai_decision': decision
    }), 201

@loan_bp.route('/my-loans', methods=['GET'])
def my_loans():
    """
    Fetch all loans for the authenticated user.
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

    loans = Loan.query.filter_by(customer_id=user_id).order_by(Loan.applied_at.desc()).all()
    
    loans_list = []
    for l in loans:
        loans_list.append({
            'id': l.id,
            'loan_type': l.loan_type,
            'amount': float(l.amount) if l.amount else 0,
            'status': l.status,
            'interest_rate': float(l.interest_rate) if l.interest_rate else None,
            'max_approved_emi': float(l.max_approved_emi) if l.max_approved_emi else None,
            'applied_at': l.applied_at.isoformat()
        })
        
    return jsonify(loans_list), 200
