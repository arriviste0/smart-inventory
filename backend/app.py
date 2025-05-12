from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-here')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# Initialize Firebase Admin
cred = credentials.Certificate('./serviceAccountKey.json')  # Make sure to download and place the service account key here
firebase_admin.initialize_app(cred, {
    'projectId': 'smart-inventory-fe1f6',
    'storageBucket': 'smart-inventory-fe1f6.firebasestorage.app'
})
db = firestore.client()

# Initialize JWT
jwt = JWTManager(app)

# Import routes
from routes.auth import auth_bp
from routes.inventory import inventory_bp
from routes.notifications import notifications_bp
from routes.analytics import analytics_bp
from routes.users import users_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
app.register_blueprint(notifications_bp, url_prefix='/api/notifications')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(users_bp, url_prefix='/api/users')

if __name__ == '__main__':
    app.run(debug=True) 