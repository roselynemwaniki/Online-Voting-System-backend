from flask_sqlalchemy import SQLAlchemy
from extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default="voter")
    is_approved = db.Column(db.Boolean, default=False)

    # Relationship to votes
    votes = db.relationship('Vote', backref='voter', cascade="all, delete", lazy=True)


class Election(db.Model):
    __tablename__ = 'elections'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    # Relationship to candidates & votes
    candidates = db.relationship('Candidate', backref='election', cascade="all, delete", lazy=True)
    votes = db.relationship('Vote', backref='election', cascade="all, delete", lazy=True)
    results = db.relationship('Result', backref='election', cascade="all, delete", lazy=True)


class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)

    # Relationship to results
    results = db.relationship('Result', backref='candidate', cascade="all, delete", lazy=True)


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    choice = db.Column(db.String(100), nullable=False)


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    total_votes = db.Column(db.Integer, default=0)
