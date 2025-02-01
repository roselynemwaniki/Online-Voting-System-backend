from flask import Blueprint, jsonify, request
from models import db, Vote
from flask_jwt_extended import jwt_required, get_jwt_identity

vote_bp = Blueprint('vote', __name__)

# CREATE: Cast a vote
@vote_bp.route('/vote', methods=['POST'])
@jwt_required()
def cast_vote():
    data = request.json
    user_id = get_jwt_identity()  # Get the current user ID from the JWT token
    vote = Vote(
        voter_id=user_id,
        election_id=data['election_id'],
        choice=data['choice']
    )
    db.session.add(vote)
    db.session.commit()
    return jsonify({"message": "Vote cast successfully"}), 201

# READ: Get all votes for a specific election
@vote_bp.route('/votes/<int:election_id>', methods=['GET'])
def get_votes(election_id):
    votes = Vote.query.filter_by(election_id=election_id).all()
    return jsonify([{
        "voter_id": vote.voter_id,
        "choice": vote.choice
    } for vote in votes]), 200

# DELETE: Delete a vote
@vote_bp.route('/vote/<int:vote_id>', methods=['DELETE'])
def delete_vote(vote_id):
    vote = Vote.query.get(vote_id)
    if not vote:
        return jsonify({"error": "Vote not found"}), 404

    db.session.delete(vote)
    db.session.commit()
    return jsonify({"message": "Vote deleted successfully"}), 200
