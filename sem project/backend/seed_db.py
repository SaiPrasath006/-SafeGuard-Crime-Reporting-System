import os
import sys

# Ensure backend path is in python path
base_dir = os.path.dirname(os.path.abspath(__file__))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from app import create_app, db, bcrypt
from models.models import User, CrimeReport, Evidence, StatusHistory
from datetime import datetime, timedelta

def seed_database(reset=True):
    app = create_app()
    with app.app_context():
        if reset:
            print("Resetting database tables...")
            db.drop_all()

        print(f"Creating database tables on: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()


        # Seed Users
        users_data = [
            {
                "username": "admin",
                "email": "admin@safeguard.gov",
                "password": "admin123",
                "full_name": "Chief Administrator",
                "phone_number": "+1-800-555-0100",
                "role": "admin"
            },
            {
                "username": "officer_smith",
                "email": "smith@police.gov",
                "password": "officer123",
                "full_name": "Inspector James Smith",
                "phone_number": "+1-800-555-0199",
                "role": "officer"
            },
            {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "password": "user123",
                "full_name": "John Doe",
                "phone_number": "+1-555-0198",
                "role": "user"
            },
            {
                "username": "sarah_connor",
                "email": "sarah.connor@example.com",
                "password": "user123",
                "full_name": "Sarah Connor",
                "phone_number": "+1-555-0144",
                "role": "user"
            }
        ]

        user_instances = {}
        for u in users_data:
            existing = User.query.filter_by(username=u["username"]).first()
            if not existing:
                hashed = bcrypt.generate_password_hash(u["password"]).decode('utf-8')
                new_u = User(
                    username=u["username"],
                    email=u["email"],
                    password=hashed,
                    full_name=u["full_name"],
                    phone_number=u["phone_number"],
                    role=u["role"]
                )
                db.session.add(new_u)
                db.session.flush()
                user_instances[u["username"]] = new_u
                print(f" Created user: {u['username']} ({u['role']})")
            else:
                user_instances[u["username"]] = existing
                print(f" User already exists: {u['username']}")

        db.session.commit()

        # Seed Crime Reports if empty
        if CrimeReport.query.count() == 0:
            john = user_instances.get("john_doe")
            sarah = user_instances.get("sarah_connor")

            crimes = [
                {
                    "tracking_id": "OCR-A109F2B8",
                    "user_id": john.id if john else None,
                    "title": "Phishing & Banking Cyber Fraud",
                    "description": "Received a fraudulent SMS claiming to be from Central Bank requesting OTP. $450 was unlawfully debited from my account.",
                    "category": "Cybercrime",
                    "severity": "High",
                    "location": "742 Evergreen Terrace, Sector 4",
                    "status": "Under Review",
                    "is_anonymous": False,
                    "phone_number": "+1-555-0198",
                    "aadhar": "XXXX-XXXX-4921",
                    "created_offset": 5,
                    "evidence": [
                        ("OCR-A109F2B8_bank_transaction_receipt.pdf", "application/pdf", 102400)
                    ],
                    "history": [
                        ("Submitted", "Complaint registered via citizen portal.", "Citizen (John Doe)"),
                        ("Under Review", "Assigned to Cyber Crime Cell team for investigation.", "officer_smith")
                    ]
                },
                {
                    "tracking_id": "OCR-B77C4E10",
                    "user_id": sarah.id if sarah else None,
                    "title": "Stolen Mountain Bike outside Metro Station",
                    "description": "Trek Marlin 7 blue mountain bike was stolen from the bicycle rack between 4:00 PM and 6:30 PM.",
                    "category": "Theft",
                    "severity": "Medium",
                    "location": "Central Metro Station Gate 2",
                    "status": "Submitted",
                    "is_anonymous": False,
                    "phone_number": "+1-555-0144",
                    "aadhar": "XXXX-XXXX-8812",
                    "created_offset": 2,
                    "evidence": [
                        ("OCR-B77C4E10_bike_purchase_invoice.jpg", "image/jpeg", 204800)
                    ],
                    "history": [
                        ("Submitted", "Complaint filed online with purchase invoice details.", "Citizen (Sarah Connor)")
                    ]
                },
                {
                    "tracking_id": "OCR-C3910AA4",
                    "user_id": john.id if john else None,
                    "title": "Armed Robbery at Convenience Store",
                    "description": "Witnessed an armed robbery at 24/7 Express Store by two masked individuals at approximately 11:15 PM.",
                    "category": "Armed Robbery",
                    "severity": "Critical",
                    "location": "Corner of 5th Ave & Main Street",
                    "status": "Investigating",
                    "is_anonymous": False,
                    "phone_number": "+1-555-0198",
                    "aadhar": "XXXX-XXXX-4921",
                    "created_offset": 10,
                    "evidence": [
                        ("OCR-C3910AA4_cctv_surveillance_frame.png", "image/png", 512000)
                    ],
                    "history": [
                        ("Submitted", "Emergency incident report logged.", "Citizen (John Doe)"),
                        ("Under Review", "Patrol team dispatched to scene.", "admin"),
                        ("Investigating", "CCTV footage retrieved from nearby surveillance cameras.", "officer_smith")
                    ]
                },
                {
                    "tracking_id": "OCR-D883011F",
                    "user_id": sarah.id if sarah else None,
                    "title": "Vandalism and Property Damage in Park",
                    "description": "Public benches and park signs tagged with spray paint and damaged overnight.",
                    "category": "Vandalism",
                    "severity": "Low",
                    "location": "Oakwood Community Park",
                    "status": "Resolved",
                    "is_anonymous": True,
                    "phone_number": "N/A",
                    "aadhar": "N/A",
                    "created_offset": 14,
                    "evidence": [],
                    "history": [
                        ("Submitted", "Anonymous report received.", "Anonymous Citizen"),
                        ("Under Review", "Forwarded to Municipal Parks & Police Department.", "admin"),
                        ("Resolved", "Clean-up team dispatched and patrol increased.", "officer_smith")
                    ]
                }
            ]

            for c in crimes:
                created_time = datetime.utcnow() - timedelta(days=c["created_offset"])
                report = CrimeReport(
                    tracking_id=c["tracking_id"],
                    user_id=c["user_id"],
                    title=c["title"],
                    description=c["description"],
                    category=c["category"],
                    severity=c["severity"],
                    location=c["location"],
                    status=c["status"],
                    is_anonymous=c["is_anonymous"],
                    phone_number=c["phone_number"],
                    aadhar=c["aadhar"],
                    created_at=created_time,
                    updated_at=created_time
                )
                db.session.add(report)
                db.session.flush()

                # Seed Evidence records
                for e_path, e_type, e_size in c.get("evidence", []):
                    ev_rec = Evidence(
                        report_id=report.id,
                        file_path=e_path,
                        file_type=e_type,
                        file_size=e_size,
                        uploaded_at=created_time
                    )
                    db.session.add(ev_rec)

                for h_status, h_comment, h_by in c["history"]:
                    h_log = StatusHistory(
                        report_id=report.id,
                        status=h_status,
                        comment=h_comment,
                        updated_by=h_by,
                        timestamp=created_time
                    )
                    db.session.add(h_log)

                print(f" Created report: {c['tracking_id']} - {c['title']} ({c['status']})")

            db.session.commit()
            print("Successfully seeded crime reports, evidence records, and history logs.")


        print("\nDatabase initialization & seeding completed successfully!")
        print("Sample Login Credentials:")
        print(" -> Admin Account:   Username: admin         / Password: admin123")
        print(" -> Officer Account: Username: officer_smith / Password: officer123")
        print(" -> Citizen User 1:  Username: john_doe      / Password: user123")
        print(" -> Citizen User 2:  Username: sarah_connor   / Password: user123")

if __name__ == "__main__":
    seed_database()
