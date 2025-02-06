from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from extensions import db  

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['SECRET_KEY'] = 'your_secure_random_secret_key'

    # Initialize extensions
    db.init_app(app)  # Ensure SQLAlchemy is initialized correctly
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)

    # Import models after initializing db
    from models import User, Election, Candidate, Vote, Result

    # Register Blueprints
    from views.user import user_bp
    from views.election import election_bp
    from views.vote import vote_bp
    from views.results import result_bp
    from views.candidate import candidate_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(election_bp)
    app.register_blueprint(vote_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(candidate_bp)

    return app

app = create_app()
# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)

