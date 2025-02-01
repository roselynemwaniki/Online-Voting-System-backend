from flask import Blueprint, jsonify, request
from models import db, Election

election_bp = Blueprint('election', __name__)

# CREATE: Add new election
@election_bp.route('/election', methods=['POST'])
def create_election():
    data = request.json
    required_fields = ['title', 'start_date', 'end_date']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
    try:
        election = Election(
            title=data['title'],
            description=data.get('description', ''),
            start_date=data['start_date'],
            end_date=data['end_date'],
            is_active=data.get('is_active', False)
        )
        db.session.add(election)
        db.session.commit()
        return jsonify({"message": "Election created successfully", "election": {
            "id": election.id,
            "title": election.title,
            "description": election.description,
            "start_date": election.start_date,
            "end_date": election.end_date,
            "is_active": election.is_active
        }}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the election", "details": str(e)}), 500


# # READ: Get candidates for a specific election
# @election_bp.route('/candidates/<int:election_id>', methods=['GET'])
# def get_candidates(election_id):
#     candidates = Candidate.query.filter_by(election_id=election_id).all()
#     return jsonify([{
#         "id": candidate.id,
#         "name": candidate.name,
#         "election_id": candidate.election_id
#     } for candidate in candidates]), 200

# READ: Get all elections
@election_bp.route('/elections', methods=['GET'])
def get_elections():
    elections = Election.query.all()
    return jsonify([{
        "id": election.id,
        "title": election.title,
        "description": election.description,
        "start_date": election.start_date,
        "end_date": election.end_date,
        "is_active": election.is_active
    } for election in elections]), 200

# UPDATE: Update election details
@election_bp.route('/election/<int:election_id>', methods=['PUT'])
def update_election(election_id):
    data = request.json
    election = Election.query.get(election_id)
    if not election:
        return jsonify({"error": "Election not found"}), 404

    election.title = data.get('title', election.title)
    election.description = data.get('description', election.description)
    election.start_date = data.get('start_date', election.start_date)
    election.end_date = data.get('end_date', election.end_date)
    election.is_active = data.get('is_active', election.is_active)

    db.session.commit()
    return jsonify({"message": "Election updated successfully"}), 200

# DELETE: Delete an election
@election_bp.route('/election/<int:election_id>', methods=['DELETE'])
def delete_election(election_id):
    election = Election.query.get(election_id)
    if not election:
        return jsonify({"error": "Election not found"}), 404

    db.session.delete(election)
    db.session.commit()
    return jsonify({"message": "Election deleted successfully"}), 200
