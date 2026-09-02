from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), default='user') # 'user', 'officer', 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name or self.username,
            "phone_number": self.phone_number or "N/A",
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class CrimeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for anonymous
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50), default='Medium') # Low, Medium, High, Critical
    location = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default='Submitted') # Submitted, Under Review, Investigating, Resolved, Closed
    is_anonymous = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(20), nullable=True)
    aadhar = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    reporter = db.relationship('User', backref='reports', lazy=True)
    evidence = db.relationship('Evidence', backref='report', cascade="all, delete-orphan", lazy=True)
    status_history = db.relationship('StatusHistory', backref='report', cascade="all, delete-orphan", lazy=True, order_by="StatusHistory.timestamp.desc()")

    def to_dict(self, include_reporter=True):
        data = {
            "id": self.id,
            "tracking_id": self.tracking_id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "severity": self.severity,
            "location": self.location,
            "status": self.status,
            "is_anonymous": self.is_anonymous,
            "phone_number": self.phone_number,
            "aadhar": self.aadhar,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "evidence": [e.to_dict() for e in self.evidence],
            "status_history": [sh.to_dict() for sh in self.status_history]
        }

        if include_reporter:
            if self.is_anonymous:
                data["reporter"] = {
                    "username": "Anonymous",
                    "full_name": "Anonymous Citizen",
                    "email": "Hidden",
                    "phone_number": "Hidden"
                }
            elif self.reporter:
                data["reporter"] = self.reporter.to_dict()
            else:
                data["reporter"] = {
                    "username": "Guest User",
                    "full_name": "Non-registered Guest",
                    "email": "Not provided",
                    "phone_number": self.phone_number or "Not provided"
                }
        return data

class Evidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('crime_report.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "file_path": self.file_path,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class StatusHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('crime_report.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text, nullable=True)
    updated_by = db.Column(db.String(80), default='System')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "status": self.status,
            "comment": self.comment,
            "updated_by": self.updated_by,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

