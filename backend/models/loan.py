from extensions import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loans'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    
    # Financial Details
    loan_type = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    purpose = db.Column(db.String(255))
    term_months = db.Column(db.Integer, nullable=False)
    
    # Applicant Profile (Snapshot at time of application)
    income = db.Column(db.Numeric(15, 2))
    employment_type = db.Column(db.String(50))
    existing_emi = db.Column(db.Numeric(15, 2))
    pan_number = db.Column(db.String(20), nullable=True)
    aadhaar_number = db.Column(db.String(20), nullable=True)
    id_document_name = db.Column(db.String(100), nullable=True)
    income_document_name = db.Column(db.String(100), nullable=True)
    
    # AI Decision Output
    status = db.Column(db.String(20), default='PENDING') # PENDING, APPROVED, REJECTED
    ai_score = db.Column(db.Integer)
    ai_confidence = db.Column(db.Numeric(5, 2))
    interest_rate = db.Column(db.Numeric(5, 2))
    max_approved_emi = db.Column(db.Numeric(15, 2))
    repaid_emis = db.Column(db.Integer, default=0)
    outstanding_balance = db.Column(db.Numeric(15, 2))
    
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documents = db.relationship('Document', backref='loan', lazy=True, cascade="all, delete-orphan")


class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.id', ondelete='SET NULL'), nullable=True)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='PENDING') # PENDING, PROCESSING, VERIFIED
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
