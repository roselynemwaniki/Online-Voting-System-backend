from flask import Flask, request, jsonify
from models import db, User, Election, Vote, Candidate, Result
from backend.utils import generate_token, verify_token, hash_password, check_password
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

def register_routes(app):
    from views.user import user_bp
    from views.election import election_bp
    from views.candidate import candidate_bp
    from views.vote import vote_bp
    from views.results import result_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(election_bp, url_prefix='/api')
    app.register_blueprint(candidate_bp, url_prefix='/api')
    app.register_blueprint(vote_bp, url_prefix='/api')
    app.register_blueprint(result_bp, url_prefix='/api')

    # User Registration
    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json
        required_fields = ['name', 'email', 'password']
        if not all(k in data for k in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already registered"}), 409

        hashed_password = hash_password(data['password'])
        user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data.get('role', 'voter'),
            is_approved=False  # New users require admin approval
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully. Awaiting admin approval."}), 201

    # User Login with Approval Check
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password(data['password'], user.password):
            return jsonify({"error": "Invalid credentials"}), 401

        if not user.is_approved:
            return jsonify({"message": "Your account is not approved yet."}), 403

        token = generate_token({"id": user.id, "role": user.role})
        return jsonify({"token": token, "role": user.role}), 200

    # View Active Elections (Voter)
    @app.route('/api/elections', methods=['GET'])
    @jwt_required()
    def get_elections():
        elections = Election.query.filter_by(is_active=True).all()
        result = [{"id": e.id, "title": e.title, "description": e.description} for e in elections]
        return jsonify(result), 200

    # Create Election (Admin Only)
    @app.route('/api/elections', methods=['POST'])
    @jwt_required()
    def create_election():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.json
        if not all(field in data for field in ['title', 'description', 'start_date', 'end_date']):
            return jsonify({"error": "Missing required fields"}), 400

        try:
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%S')
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%dT%H:%M:%S')

            election = Election(
                title=data['title'],
                description=data['description'],
                start_date=start_date,
                end_date=end_date
            )

            db.session.add(election)
            db.session.commit()

            return jsonify({
                "message": "Election created successfully",
                "election": {
                    "id": election.id,
                    "title": election.title,
                    "description": election.description,
                    "start_date": election.start_date,
                    "end_date": election.end_date
                }
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # Cast a Vote (Voter Only)
    @app.route('/api/vote', methods=['POST'])
    @jwt_required()
    def cast_vote():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "voter":
            return jsonify({"error": "Only voters can cast a vote"}), 403

        data = request.json
        existing_vote = Vote.query.filter_by(voter_id=user_id, election_id=data['election_id']).first()
        if existing_vote:
            return jsonify({"error": "You have already voted in this election"}), 409

        vote = Vote(
            voter_id=user_id,
            election_id=data['election_id'],
            choice=data['choice']
        )
        db.session.add(vote)
        db.session.commit()
        return jsonify({"message": "Vote cast successfully"}), 201

    # Get Election Results
    @app.route('/api/elections/<int:election_id>/results', methods=['GET'])
    @jwt_required()
    def get_results(election_id):
        results = Result.query.filter_by(election_id=election_id).all()
        if not results:
            return jsonify({"error": "Results not found"}), 404

        result_data = [{"candidate": r.candidate, "total_votes": r.total_votes} for r in results]
        return jsonify(result_data), 200

    # Register Candidates (Admin Only)
    @app.route('/api/elections/<int:election_id>/candidates', methods=['POST'])
    @jwt_required()
    def add_candidate(election_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user or user.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        data = request.json
        candidate = Candidate(
            name=data['name'],
            election_id=election_id
        )
        db.session.add(candidate)
        db.session.commit()
        return jsonify({"message": "Candidate added successfully"}), 201

    # Approve User (Admin Only)
    @app.route('/api/users/<int:user_id>/approve', methods=['POST'])
    @jwt_required()
    def approve_user(user_id):
        admin_id = get_jwt_identity()
        admin = User.query.get(admin_id)

        if not admin or admin.role != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.is_approved = True
        db.session.commit()
        return jsonify({"message": "User approved successfully"}), 200

    # Error handler for method not allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed for this endpoint."}), 405
