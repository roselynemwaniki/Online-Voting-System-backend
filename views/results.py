from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Result, Vote, User

result_bp = Blueprint('result', __name__)

# CREATE: Add result for an election
@result_bp.route('/result', methods=['POST'])
@jwt_required()
def add_result():
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json
    result = Result(
        election_id=data['election_id'],
        candidate=data['candidate'],
        total_votes=data['total_votes'],
        winner=data.get('winner', '')
    )
    db.session.add(result)
    db.session.commit()
    return jsonify({"message": "Result added successfully"}), 201

# READ: Get results for a specific election
@result_bp.route('/results/<int:election_id>', methods=['GET'])
@jwt_required()
def get_results(election_id):
    results = Result.query.filter_by(election_id=election_id).all()
    return jsonify([{
        "candidate": result.candidate,
        "total_votes": result.total_votes,
        "winner": result.winner
    } for result in results]), 200

# UPDATE: Update result for a candidate
@result_bp.route('/result/<int:result_id>', methods=['PUT'])
@jwt_required()
def update_result(result_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json
    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    result.candidate = data.get('candidate', result.candidate)
    result.total_votes = data.get('total_votes', result.total_votes)
    result.winner = data.get('winner', result.winner)

    db.session.commit()
    return jsonify({"message": "Result updated successfully"}), 200

# TURNOUT: Monitor voter turnout for an election
@result_bp.route('/turnout/<int:election_id>', methods=['GET'])
@jwt_required()
def voter_turnout(election_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    turnout = Vote.query.filter_by(election_id=election_id).count()
    return jsonify({'election_id': election_id, 'turnout': turnout}), 200

# DELETE: Delete a result
@result_bp.route('/result/<int:result_id>', methods=['DELETE'])
@jwt_required()
def delete_result(result_id):
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if admin.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403

    result = Result.query.get(result_id)
    if not result:
        return jsonify({"error": "Result not found"}), 404

    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "Result deleted successfully"}), 200
