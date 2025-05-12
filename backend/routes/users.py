from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import firebase_admin
from firebase_admin import auth as firebase_auth
from app import db

users_bp = Blueprint('users', __name__)

# Helper to check if current user is admin (by custom claim)
def is_admin(uid):
    try:
        user = firebase_auth.get_user(uid)
        claims = user.custom_claims or {}
        return claims.get('role') == 'admin'
    except Exception:
        return False

@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    current_uid = get_jwt_identity()
    if not is_admin(current_uid):
        return jsonify({'error': 'Admin privileges required'}), 403

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'employee')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        user_record = firebase_auth.create_user(
            email=email,
            password=password
        )
        # Set custom claim for role
        firebase_auth.set_custom_user_claims(user_record.uid, {'role': role})
        return jsonify({
            'message': 'User created successfully',
            'email': email,
            'password': password,
            'role': role
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400 