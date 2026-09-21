import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import jwt
from config import Config
from extensions import db
from models.user import User
from models.loan import Document

document_bp = Blueprint('document', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@document_bp.route('/upload', methods=['POST'])
def upload_document():
    # 1. Authenticate
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized access'}), 401
    
    token = auth_header.split(" ")[1]
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']
    except Exception:
        return jsonify({'error': 'Invalid session'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    doc_type = request.form.get('document_type', 'General')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add user id to filename to make it unique
        unique_filename = f"user_{user_id}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Simulate AI OCR verification logic
        # In a real app, this would call Tesseract or AWS Textract
        status = 'VERIFIED' # Auto-verify for the demo
        
        # Save to DB
        new_doc = Document(
            customer_id=user_id,
            document_type=doc_type,
            file_path=file_path,
            status=status
        )
        db.session.add(new_doc)
        db.session.commit()
        
        return jsonify({
            'message': 'File uploaded and verified successfully',
            'document': {
                'id': new_doc.id,
                'document_type': new_doc.document_type,
                'status': new_doc.status
            }
        }), 201
        
    return jsonify({'error': 'File type not allowed'}), 400

@document_bp.route('/my-documents', methods=['GET'])
def my_documents():
    # Authenticate
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized access'}), 401
    
    token = auth_header.split(" ")[1]
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']
    except Exception:
        return jsonify({'error': 'Invalid session'}), 401
        
    docs = Document.query.filter_by(customer_id=user_id).all()
    
    doc_list = []
    for d in docs:
        doc_list.append({
            'id': d.id,
            'document_type': d.document_type,
            'status': d.status,
            'uploaded_at': d.uploaded_at.isoformat()
        })
        
    return jsonify(doc_list), 200
