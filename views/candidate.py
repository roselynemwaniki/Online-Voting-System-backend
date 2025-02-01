from flask import Blueprint, jsonify, request
from models import db, Candidate
from flask_jwt_extended import jwt_required, get_jwt_identity

candidate_bp = Blueprint('candidate', __name__)

# CREATE: Add a new candidate
@candidate_bp.route('/candidates', methods=['POST'])
@jwt_required()
def add_candidate():
    data = request.json
    required_fields = ['name', 'election_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    candidate = Candidate(
        name=data['name'],
        election_id=data['election_id']
    )
    db.session.add(candidate)
    db.session.commit()
    return jsonify({"message": "Candidate added successfully"}), 201

# READ: Get all candidates for a specific election
@candidate_bp.route('/elections/<int:election_id>/candidates', methods=['GET'])
def get_candidates(election_id):
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    return jsonify([{
        "id": candidate.id,
        "name": candidate.name,
        "election_id": candidate.election_id
    } for candidate in candidates]), 200

# DELETE: Delete a candidate
@candidate_bp.route('/candidates/<int:candidate_id>', methods=['DELETE'])
@jwt_required()
def delete_candidate(candidate_id):
    candidate = Candidate.query.get(candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    db.session.delete(candidate)
    db.session.commit()
    return jsonify({"message": "Candidate deleted successfully"}), 200
