from flask import Blueprint, request, jsonify
from models.notification import Notification
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

notification_routes = Blueprint('notifications', __name__)

@notification_routes.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()
    filter_type = request.args.get('filter', 'all')
    show_unread = request.args.get('unread', 'false').lower() == 'true'
    
    query = Notification.query.filter_by(user_id=user_id)
    
    if show_unread:
        query = query.filter_by(is_read=False)
    
    if filter_type != 'all':
        query = query.filter_by(priority=filter_type)
    
    notifications = query.order_by(Notification.created_at.desc()).all()
    return jsonify([notif.to_dict() for notif in notifications])

@notification_routes.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    user_id = get_jwt_identity()
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify(notification.to_dict())

@notification_routes.route('/mark-all-read', methods=['PUT'])
@jwt_required()
def mark_all_as_read():
    user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()
    
    return jsonify({'message': 'All notifications marked as read'})

@notification_routes.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    user_id = get_jwt_identity()
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    db.session.delete(notification)
    db.session.commit()
    
    return jsonify({'message': 'Notification deleted'})

@notification_routes.route('/clear-all', methods=['DELETE'])
@jwt_required()
def clear_all_notifications():
    user_id = get_jwt_identity()
    Notification.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({'message': 'All notifications cleared'})

@notification_routes.route('/', methods=['POST'])
@jwt_required()
def create_notification():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['type', 'title', 'message', 'priority']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    notification = Notification(
        type=data['type'],
        title=data['title'],
        message=data['message'],
        priority=data['priority'],
        user_id=user_id
    )
    
    db.session.add(notification)
    db.session.commit()
    
    return jsonify(notification.to_dict()), 201 