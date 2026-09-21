import os
from app import create_app
from extensions import db
from models.user import User, Customer
from models.loan import Loan, Document

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database initialized successfully!")
