from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    # Set up paths for serving frontend
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dir = os.path.join(os.path.dirname(base_dir), 'frontend')
    
    app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
    
    # Configuration
    instance_dir = os.path.join(base_dir, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        
    db_path = os.path.join(instance_dir, 'crime_system.db').replace('\\', '/')
    default_db_uri = f'sqlite:///{db_path}'
    
    raw_db_uri = os.getenv('DATABASE_URL', default_db_uri)
    if raw_db_uri.startswith('sqlite:///'):
        sqlite_file = raw_db_uri.replace('sqlite:///', '')
        if not os.path.isabs(sqlite_file):
            sqlite_file = os.path.join(base_dir, sqlite_file)
        sqlite_file = os.path.normpath(sqlite_file).replace('\\', '/')
        raw_db_uri = f'sqlite:///{sqlite_file}'

    app.config['SQLALCHEMY_DATABASE_URI'] = raw_db_uri

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'safeguard-super-secret-jwt-key-2026')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'uploads')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])


    # Initialize extensions
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints (to be created)
    from routes.auth import auth_bp
    from routes.reports import report_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(report_bp, url_prefix='/api/reports')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    with app.app_context():
        try:
            db.create_all()
            from models.models import User
            if not User.query.filter_by(username='admin').first():
                admin_user = User(
                    username='admin',
                    email='admin@safeguard.com',
                    password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                    full_name='System Admin',
                    role='admin'
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Default admin verified: admin / admin123")
        except Exception as e:
            print(f"Note on initial db check: {e}")


    # Serve portal.html at root
    @app.route('/')
    def index():
        return app.send_static_file('portal.html')

    # Serve uploaded evidence files
    from flask import send_from_directory
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
