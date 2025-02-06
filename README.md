# Backend for Online Voting System

## Overview
The Online Voting System backend is built using Flask. It provides the necessary APIs for user management, election management, voting, and result tracking. This system aims to facilitate a secure and efficient voting process for users, ensuring transparency and accessibility.

## Features
✅ User Features
- **User Registration & Authentication**: Secure authentication system for users, allowing them to register and log in.
- **Election Creation & Management**: Create and manage elections with ease.
- **Candidate Management**: Add and manage candidates for elections, ensuring a fair selection process.
- **Voting Functionality**: Allow users to cast their votes securely and anonymously.
- **Result Management**: Track and manage election results in real-time.
- **JWT-based Authentication**: Secure access to the APIs using JSON Web Tokens.

## Tech Stack
🔹 Backend
- **Framework**: Flask (version 2.0.1)
- **Database**: SQLite (with SQLAlchemy version 1.4.22)
- **Authentication**: Flask-JWT-Extended (version 4.3.1)
- **CORS**: Flask-CORS for handling cross-origin requests

## Installation & Setup
🔹 Backend Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/voting-system.git
   cd voting-system/backend
   ```


2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the migrations** (if using Flask-Migrate):
   ```bash
   flask db upgrade
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```
   The backend will be available at `http://localhost:5000`.

## API Endpoints
### User Management
- **Register User**: `POST /user`
  - **Request**: `{ "username": "user1", "password": "pass123" }`
  - **Response**: `{ "message": "User registered successfully." }`
  
- **Login User**: `POST /login`
  - **Request**: `{ "username": "user1", "password": "pass123" }`
  - **Response**: `{ "access_token": "your_jwt_token" }`

- **Get All Users**: `GET /users` (Admin only)
- **Update User**: `PUT /user/<user_id>` (Admin only)
- **Delete User**: `DELETE /user/<user_id>` (Admin only)
- **Approve Voter**: `PATCH /approve_voter/<user_id>` (Admin only)

### Election Management
- **Create Election**: `POST /election`
- **Get All Elections**: `GET /elections`
- **Update Election**: `PUT /election/<election_id>`
- **Delete Election**: `DELETE /election/<election_id>`

### Candidate Management
- **Add Candidate**: `POST /candidates`
- **Get Candidates for Election**: `GET /elections/<election_id>/candidates`
- **Delete Candidate**: `DELETE /candidates/<candidate_id>`

### Voting Management
- **Cast Vote**: `POST /vote`
- **Get Votes for Election**: `GET /votes/<election_id>`
- **Delete Vote**: `DELETE /vote/<vote_id>`

### Result Management
- **Add Result**: `POST /result`
- **Get Results for Election**: `GET /results/<election_id>`
- **Update Result**: `PUT /result/<result_id>`
- **Monitor Voter Turnout**: `GET /turnout/<election_id>`
- **Delete Result**: `DELETE /result/<result_id>`

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
