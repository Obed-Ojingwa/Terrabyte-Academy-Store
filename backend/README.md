# Terrabyte Academy Store Backend

This is the backend for the Terrabyte Academy Store application, built with FastAPI, Python, and SQLAlchemy.

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
   - Copy `.env.example` to `.env` and adjust the values as needed
   - For development, you can use the provided `.env` file

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Run tests:
   ```bash
   pytest
   ```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Features

- User authentication (registration, login, JWT tokens, email verification)
- Role-based access control (Admin, Seller, Customer)
- Product catalog management
- Shopping cart and order management
- Training academy system
- Seller system
- Content management (blog, reviews, FAQ)
- Advanced features (wishlist, notifications, coupons)
- Password reset functionality
- Email service integration

## Email Service

The email service is designed to work in both development and production environments:

- In development (when SMTP settings are not configured), emails are logged to the console
- In production (when SMTP settings are configured), actual emails are sent

To configure email for production, set the following environment variables in your `.env` file:
- SMTP_HOST
- SMTP_PORT
- SMTP_TLS
- SMTP_USER
- SMTP_PASSWORD
- EMAILS_FROM_EMAIL
- EMAILS_FROM_NAME

## Database

The application uses SQLAlchemy with Alembic for database migrations.

To create the database tables:
```bash
python migrate.py
```

To generate a new migration:
```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
python migrate.py
```