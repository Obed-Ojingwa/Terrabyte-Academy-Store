from typing import List, Optional
from pydantic import EmailStr
from app.core.config import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_tls = settings.SMTP_TLS
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.emails_from_email = settings.EMAILS_FROM_EMAIL
        self.emails_from_name = settings.EMAILS_FROM_NAME

    async def send_email(
        self,
        email_to: EmailStr,
        subject: str,
        body: str,
        body_type: str = "html"
    ) -> bool:
        """
        Send an email.

        Args:
            email_to: Recipient email address
            subject: Email subject
            body: Email body content
            body_type: Either "plain" or "html"

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        # If email settings are not configured, just log the email (for development)
        if not self.smtp_host or not self.smtp_port or not self.smtp_user:
            logger.info(f"Email would be sent to {email_to}: {subject}")
            logger.debug(f"Email body: {body}")
            # In development, we'll pretend it worked
            return True

        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = f"{self.emails_from_name} <{self.emails_from_email}>"
            message["To"] = email_to
            message["Subject"] = subject

            # Attach body
            message.attach(MIMEText(body, body_type))

            # Create SMTP session
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            if self.smtp_tls:
                server.starttls()
            server.login(self.smtp_user, self.smtp_password)

            # Send email
            text = message.as_string()
            server.sendmail(self.emails_from_email, email_to, text)
            server.quit()

            logger.info(f"Email sent successfully to {email_to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {email_to}: {str(e)}")
            return False

    async def send_verification_email(self, email_to: EmailStr, verification_token: str) -> bool:
        """
        Send email verification email.

        Args:
            email_to: Recipient email address
            verification_token: Email verification token

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = "Verify Your Email - Terrabyte Academy Store"
        # In a real application, you would have a frontend URL for verification
        verification_url = f"http://localhost:3000/verify-email?token={verification_token}"

        body = f"""
        <html>
        <body>
            <h2>Welcome to Terrabyte Academy Store!</h2>
            <p>Thank you for registering. Please click the link below to verify your email address:</p>
            <a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Verify Email</a>
            <p>Or copy and paste this URL in your browser:</p>
            <p>{verification_url}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't create an account, please ignore this email.</p>
        </body>
        </html>
        """

        return await self.send_email(email_to, subject, body, "html")

    async def send_password_reset_email(self, email_to: EmailStr, reset_token: str) -> bool:
        """
        Send password reset email.

        Args:
            email_to: Recipient email address
            reset_token: Password reset token

        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        subject = "Reset Your Password - Terrabyte Academy Store"
        # In a real application, you would have a frontend URL for password reset
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}"

        body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>We received a request to reset your password for your Terrabyte Academy Store account.</p>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_url}" style="background-color: #FF9800; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">Reset Password</a>
            <p>Or copy and paste this URL in your browser:</p>
            <p>{reset_url}</p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request a password reset, please ignore this email.</p>
        </body>
        </html>
        """

        return await self.send_email(email_to, subject, body, "html")