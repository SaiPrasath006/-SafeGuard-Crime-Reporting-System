from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from models.models import CrimeReport, Evidence, User, StatusHistory
import uuid
import os
from werkzeug.utils import secure_filename

report_bp = Blueprint('reports', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'mp4', 'mkv', 'avi'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_tracking_id():
    return "OCR-" + str(uuid.uuid4().hex[:8]).upper()

@report_bp.route('/submit', methods=['POST'])
@jwt_required(optional=True)
def submit_report():
    user_id = get_jwt_identity()
    is_anonymous_req = request.form.get('is_anonymous') == 'true'

    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    location = request.form.get('location')
    severity = request.form.get('severity', 'Medium')
    phone_number = request.form.get('phone_number')
    aadhar = request.form.get('aadhar')
    
    if not all([title, description, category, location]):
        return jsonify({"msg": "Missing required fields"}), 400
        
    tracking_id = generate_tracking_id()
    new_report = CrimeReport(
        tracking_id=tracking_id,
        user_id=user_id if user_id else None,
        title=title,
        description=description,
        category=category,
        severity=severity,
        location=location,
        phone_number=phone_number,
        aadhar=aadhar,
        is_anonymous=is_anonymous_req
    )
    
    db.session.add(new_report)
    db.session.flush() # Get report ID before commit

    # Log initial status history
    initial_log = StatusHistory(
        report_id=new_report.id,
        status="Submitted",
        comment="Complaint submitted into the system.",
        updated_by="Citizen (System)" if is_anonymous_req else f"User #{user_id}"
    )
    db.session.add(initial_log)
    
    # Handle file uploads
    if 'evidence' in request.files:
        files = request.files.getlist('evidence')
        for file in files:
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"{tracking_id}_{file.filename}")
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                new_evidence = Evidence(
                    report_id=new_report.id,
                    file_path=filename,
                    file_type=file.content_type
                )
                db.session.add(new_evidence)
                
    db.session.commit()
    return jsonify({
        "msg": "Report submitted successfully", 
        "tracking_id": tracking_id,
        "report": new_report.to_dict()
    }), 201

@report_bp.route('/track/<tracking_id>', methods=['GET'])
def track_report(tracking_id):
    report = CrimeReport.query.filter_by(tracking_id=tracking_id).first()
    if not report:
        return jsonify({"msg": "Report not found"}), 404
        
    return jsonify(report.to_dict(include_reporter=not report.is_anonymous)), 200

@report_bp.route('/my-reports', methods=['GET'])
@jwt_required()
def my_reports():
    user_id = get_jwt_identity()
    reports = CrimeReport.query.filter_by(user_id=user_id).order_by(CrimeReport.created_at.desc()).all()
    return jsonify([r.to_dict(include_reporter=True) for r in reports]), 200

