# Inventory Management System Backend

This is the backend service for the Inventory Management System, built with Flask and SQLAlchemy.

## Features

- User Authentication with JWT
- Notification System with multiple delivery channels (Email, Push, In-App)
- Inventory Management
- Analytics and Reporting
- Customizable Notification Preferences

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with the following variables:
```env
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///inventory.db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- POST `/api/auth/refresh` - Refresh JWT token

### Notifications
- GET `/api/notifications/` - Get user notifications
- GET `/api/notifications/<id>` - Get specific notification
- POST `/api/notifications/<id>/mark-read` - Mark notification as read
- POST `/api/notifications/mark-all-read` - Mark all notifications as read
- DELETE `/api/notifications/<id>` - Delete notification
- GET `/api/notifications/preferences` - Get notification preferences
- POST `/api/notifications/preferences` - Update notification preferences
- GET `/api/notifications/summary` - Get notification summary

### Inventory
- GET `/api/inventory/` - Get inventory items
- POST `/api/inventory/` - Add new inventory item
- PUT `/api/inventory/<id>` - Update inventory item
- DELETE `/api/inventory/<id>` - Delete inventory item
- GET `/api/inventory/analytics` - Get inventory analytics

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8
```

### Running the Server
```bash
flask run
```

## Deployment

1. Set environment variables for production
2. Use gunicorn for production server:
```bash
gunicorn app:app
```

## Notification System

The notification system supports multiple delivery channels:

1. In-App Notifications
   - Real-time updates using database
   - Customizable preferences
   - Priority levels

2. Email Notifications
   - SMTP integration
   - HTML templates
   - Customizable delivery rules

3. Push Notifications (Optional)
   - Integration ready for Firebase Cloud Messaging
   - Can be extended for other services

### Notification Types

- Inventory Alerts
  - Low stock warnings
  - Reorder reminders
  - Stock updates

- System Notifications
  - User account updates
  - Security alerts
  - System maintenance

- Custom Notifications
  - Can be extended for specific business needs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 