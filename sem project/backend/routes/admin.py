from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db
from models.models import CrimeReport, User, Evidence, StatusHistory
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") not in ['admin', 'officer']:
            return jsonify({"msg": "Admin or Police Officer access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/reports', methods=['GET'])
@jwt_required()
@admin_required
def get_all_reports():
    category = request.args.get('category')
    status = request.args.get('status')
    
    query = CrimeReport.query
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
        
    reports = query.order_by(CrimeReport.created_at.desc()).all()
    return jsonify([r.to_dict(include_reporter=True) for r in reports]), 200

@admin_bp.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_report_details(report_id):
    report = CrimeReport.query.get_or_404(report_id)
    # Admin can always inspect reporter details regardless of anonymous flag
    data = report.to_dict(include_reporter=True)
    if report.is_anonymous and report.reporter:
        data["anonymous_override_info"] = {
            "real_username": report.reporter.username,
            "real_email": report.reporter.email,
            "real_name": report.reporter.full_name,
            "real_phone": report.reporter.phone_number
        }
    return jsonify(data), 200

@admin_bp.route('/reports/<int:report_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_status(report_id):
    data = request.get_json()
    report = CrimeReport.query.get_or_404(report_id)
    
    if not data or not data.get('status'):
        return jsonify({"msg": "Missing status"}), 400
        
    new_status = data['status']
    comment = data.get('comment', f"Status updated to {new_status}")
    
    claims = get_jwt()
    updater_name = claims.get("username", "Admin")

    report.status = new_status
    
    # Create audit log entry in StatusHistory
    status_log = StatusHistory(
        report_id=report.id,
        status=new_status,
        comment=comment,
        updated_by=updater_name
    )
    db.session.add(status_log)
    db.session.commit()
    
    return jsonify({
        "msg": "Status updated successfully", 
        "report": report.to_dict(include_reporter=True)
    }), 200

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.order_by(User.created_at.desc()).all()
    result = []
    for u in users:
        u_data = u.to_dict()
        u_data["total_reports_filed"] = len(u.reports)
        result.append(u_data)
    return jsonify(result), 200

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_user_details_and_crimes(user_id):
    user = User.query.get_or_404(user_id)
    user_data = user.to_dict()
    user_crimes = [r.to_dict(include_reporter=True) for r in user.reports]
    
    return jsonify({
        "user_information": user_data,
        "submitted_crimes": user_crimes,
        "total_crimes_count": len(user_crimes)
    }), 200

@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_stats():
    total_reports = CrimeReport.query.count()
    pending = CrimeReport.query.filter_by(status='Submitted').count()
    review = CrimeReport.query.filter_by(status='Under Review').count()
    investigating = CrimeReport.query.filter_by(status='Investigating').count()
    closed = CrimeReport.query.filter_by(status='Closed').count() + CrimeReport.query.filter_by(status='Resolved').count()
    total_users = User.query.count()
    
    return jsonify({
        "total": total_reports,
        "pending": pending,
        "under_review": review,
        "investigating": investigating,
        "closed": closed,
        "total_users": total_users
    }), 200

