from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  
from flask_migrate import Migrate  
from flask_jwt_extended import JWTManager  

# Initialize Flask app  
app = Flask(__name__)  

# Configuration settings  
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to a secure key for production  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = 'your_secure_random_secret_key'  # Secure secret key for Flask sessions

# Initialize extensions  
db = SQLAlchemy(app)  
migrate = Migrate(app, db)  
jwt = JWTManager(app)  

# Import models after db initialization  
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

# Run the app  
if __name__ == '__main__':  
    app.run(debug=True)
