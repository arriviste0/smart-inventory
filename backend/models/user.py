from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db  # This is now the Firestore client

class User:
    def __init__(self, email, username, password=None, role='user', user_id=None):
        self.id = user_id
        self.email = email
        self.username = username
        self.role = role
        self.created_at = datetime.utcnow()
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).limit(1).get()
        for doc in query:
            user_data = doc.to_dict()
            return User(
                email=user_data['email'],
                username=user_data['username'],
                role=user_data.get('role', 'user'),
                user_id=doc.id
            )
        return None

    def save(self):
        user_data = {
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'role': self.role,
            'created_at': self.created_at
        }
        if not self.id:
            # Create new user
            doc_ref = db.collection('users').document()
            doc_ref.set(user_data)
            self.id = doc_ref.id
        else:
            # Update existing user
            db.collection('users').document(self.id).update(user_data)
        return self.id

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        } 