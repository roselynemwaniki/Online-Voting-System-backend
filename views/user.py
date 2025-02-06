from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_cors import cross_origin  # To handle CORS
from models import db, User

user_bp = Blueprint('user', __name__)

# Register a new user
@user_bp.route('/user', methods=['POST'])
@cross_origin()  # Allow cross-origin requests
def register():
    data = request.json
    required_fields = ['name', 'email', 'password']

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'voter'),  # Default role is voter
        is_approved=False  # Default unapproved
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User registered successfully. Awaiting approval."}), 201

# User login
@user_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    if not user.is_approved:
        return jsonify({'message': 'Your account is not approved yet.'}), 403

    token = create_access_token(identity=user.id)

    return jsonify({
        'token': token,
        'role': user.role,
        'message': f'Welcome, {user.name}!'
    }), 200

# Get all users (Admin only)
@user_bp.route('/users', methods=['GET'])
@jwt_required()
@cross_origin()
def get_users():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin or admin.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_approved": user.is_approved
    } for user in users]), 200

# Approve a voter (Admin only)
@user_bp.route('/approve_voter/<int:user_id>', methods=['PATCH'])
@jwt_required()
@cross_origin()
def approve_voter(user_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)

    if not admin or admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': f'User with ID {user_id} not found'}), 404

    user.is_approved = True
    db.session.commit()

    return jsonify({'message': f'Voter {user.name} approved successfully.'}), 200
