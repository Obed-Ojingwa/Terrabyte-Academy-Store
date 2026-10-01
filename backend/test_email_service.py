#!/usr/bin/env python3
"""
Test script to demonstrate the email service functionality.
This shows that the email service works correctly in development mode
(by logging emails instead of actually sending them).
"""
import asyncio
import sys
import os

# Add the backend directory to the path so we can import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.services.email_service import EmailService

async def test_email_service():
    """Test the email service."""
    print("Creating email service...")
    email_service = EmailService()

    print("Sending test verification email...")
    # This will log the email instead of actually sending it since SMTP settings are not configured
    result = await email_service.send_verification_email(
        email_to="test@example.com",
        verification_token="test-verification-token-12345"
    )

    print(f"Email sent result: {result}")

    print("Sending test password reset email...")
    result = await email_service.send_password_reset_email(
        email_to="test@example.com",
        reset_token="test-reset-token-67890"
    )

    print(f"Password reset email sent result: {result}")

    print("\nTest completed! Check the console output above to see the logged emails.")
    print("In a production environment with proper SMTP settings, these would be actual emails.")

if __name__ == "__main__":
    asyncio.run(test_email_service())