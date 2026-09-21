from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='CUSTOMER')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to Customer profile
    customer_profile = db.relationship('Customer', backref='user', uselist=False, cascade="all, delete-orphan")

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    employment_status = db.Column(db.String(50))
    annual_income = db.Column(db.Numeric(15, 2))
    credit_score = db.Column(db.Integer, default=0)
    kyc_status = db.Column(db.String(20), default='PENDING')
    pan_number = db.Column(db.String(20), nullable=True)
    aadhaar_number = db.Column(db.String(20), nullable=True)
