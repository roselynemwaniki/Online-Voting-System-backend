from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User

user_bp = Blueprint('user', __name__)

# Register a new user
@user_bp.route('/user', methods=['POST'])
def register():
    data = request.json
    required_fields = ['name', 'email', 'password']

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email is already registered"}), 400

    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        role=data.get('role', 'voter'),
        is_approved=True
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User registered successfully."}), 201

# Login an existing user
@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    required_fields = ['email', 'password']

    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        if not user.is_approved:
            return jsonify({'message': 'Your account is not approved yet.'}), 403

        token = create_access_token(identity=user.id)
        return jsonify({
            'token': token,
            'role': user.role,
            'message': f'Welcome, {user.name}!'
        }), 200

    return jsonify({'message': 'Invalid email or password'}), 401

# Get all users
@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_approved": user.is_approved
    } for user in users]), 200

# Update user details
@user_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.json
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    if 'role' in data:
        user.role = data['role']
    if 'is_approved' in data:
        user.is_approved = data['is_approved']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "User updated successfully"}), 200

# Delete a user
@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({"message": "Unauthorized access"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# Approve a voter
@user_bp.route('/approve_voter/<int:user_id>', methods=['PATCH'])
@jwt_required()
def approve_voter(user_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Voter approved successfully.'}), 200