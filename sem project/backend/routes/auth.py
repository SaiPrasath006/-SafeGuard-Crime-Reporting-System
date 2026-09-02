from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db, bcrypt
from models.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password') or not data.get('email'):
        return jsonify({"msg": "Missing required fields (username, email, password)"}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already registered"}), 400
        
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        full_name=data.get('full_name', data['username']),
        phone_number=data.get('phone_number'),
        role=data.get('role', 'user')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully", "user": new_user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=data.get('username')).first()
    
    if user and bcrypt.check_password_hash(user.password, data.get('password')):
        access_token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role, "username": user.username}
        )
        return jsonify(
            access_token=access_token, 
            user=user.to_dict()
        ), 200
        
    return jsonify({"msg": "Invalid username or password"}), 401

@auth_bp.route('/profile', methods=['GET'])
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200

