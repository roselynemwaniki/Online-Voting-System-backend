# import bcrypt
# import jwt
# from datetime import datetime, timedelta

# SECRET_KEY = "your_secret_key"  # Replace with a secure key

# # Hash a password
# def hash_password(password):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# # Check a password
# def check_password(password, hashed_password):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# # Generate a JWT token
# def generate_token(data, exp_minutes=30):
#     payload = {
#         "data": data,
#         "exp": datetime.utcnow() + timedelta(minutes=exp_minutes)
#     }
#     return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# # Verify a JWT token
# def verify_token(token):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         return {"error": "Token expired"}
#     except jwt.InvalidTokenError:
#         return {"error": "Invalid token"}


from werkzeug.security import generate_password_hash, check_password_hash  

def hash_password(password):  
    return generate_password_hash(password)  

def verify_password(hashed_password, password):  
    return check_password_hash(hashed_password, password)