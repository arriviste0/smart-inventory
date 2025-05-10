from models.notification import Notification, NotificationPreference
from app import db
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class NotificationService:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.smtp_username = os.environ.get('SMTP_USERNAME')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')

    def create_notification(self, user_id, title, message, notification_type, priority='normal', metadata=None):
        """Create a new notification and deliver it based on user preferences."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            priority=priority,
            metadata=metadata
        )
        
        db.session.add(notification)
        db.session.commit()

        # Get user preferences
        preference = NotificationPreference.query.filter_by(
            user_id=user_id,
            notification_type=notification_type
        ).first()

        if preference:
            # Check if notification meets minimum priority
            if self._check_priority_threshold(priority, preference.min_priority):
                if preference.email_enabled:
                    self.send_email_notification(notification)
                if preference.push_enabled:
                    self.send_push_notification(notification)

        return notification

    def _check_priority_threshold(self, notification_priority, min_priority):
        """Check if notification priority meets the minimum threshold."""
        priority_levels = {
            'low': 0,
            'normal': 1,
            'high': 2
        }
        return priority_levels.get(notification_priority, 0) >= priority_levels.get(min_priority, 0)

    def send_email_notification(self, notification):
        """Send email notification."""
        if not all([self.smtp_username, self.smtp_password]):
            return False

        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = notification.user.email
            msg['Subject'] = f"[{notification.priority.upper()}] {notification.title}"

            body = f"""
            {notification.message}
            
            Priority: {notification.priority}
            Type: {notification.type}
            Time: {notification.created_at}
            """

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False

    def send_push_notification(self, notification):
        """Send push notification (implement with your preferred service)."""
        # Implement push notification logic here (e.g., using Firebase Cloud Messaging)
        pass

    def get_user_notifications(self, user_id, status='all', page=1, per_page=10):
        """Get paginated notifications for a user."""
        query = Notification.query.filter_by(user_id=user_id)
        
        if status != 'all':
            query = query.filter_by(status=status)
        
        return query.order_by(Notification.created_at.desc())\
                   .paginate(page=page, per_page=per_page, error_out=False)

    def mark_as_read(self, notification_id, user_id):
        """Mark a notification as read."""
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification and notification.status == 'unread':
            notification.mark_as_read()
            return True
        return False

    def delete_notification(self, notification_id, user_id):
        """Delete a notification."""
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    def update_preferences(self, user_id, preferences):
        """Update notification preferences for a user."""
        for pref_data in preferences:
            preference = NotificationPreference.query.filter_by(
                user_id=user_id,
                notification_type=pref_data['notification_type']
            ).first()

            if not preference:
                preference = NotificationPreference(user_id=user_id)

            for key, value in pref_data.items():
                if hasattr(preference, key):
                    setattr(preference, key, value)

            db.session.add(preference)
        
        db.session.commit()
        return True

    def create_inventory_notification(self, user_id, item_name, action, quantity=None):
        """Create an inventory-related notification."""
        templates = {
            'low_stock': {
                'title': f'Low Stock Alert: {item_name}',
                'message': f'The stock level for {item_name} is below the reorder point.',
                'priority': 'high'
            },
            'reorder': {
                'title': f'Reorder Reminder: {item_name}',
                'message': f'It\'s time to reorder {item_name}.',
                'priority': 'normal'
            },
            'stock_update': {
                'title': f'Stock Updated: {item_name}',
                'message': f'Stock level for {item_name} has been updated to {quantity}.',
                'priority': 'normal'
            }
        }

        template = templates.get(action)
        if template:
            return self.create_notification(
                user_id=user_id,
                title=template['title'],
                message=template['message'],
                notification_type='inventory',
                priority=template['priority'],
                metadata={
                    'item_name': item_name,
                    'action': action,
                    'quantity': quantity
                }
            )
        return None 