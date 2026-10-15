import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(recipient, subject, body, html_body=None):
    """Send an email with optional HTML formatting."""

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise ValueError(
            "Email credentials are missing. Check your .env file."
        )

    message = EmailMessage()
    message["Subject"] = subject
    SENDER_NAME = "A Little Motivation"
    message["From"] = formataddr(
        (SENDER_NAME, EMAIL_ADDRESS)
    )
    message["To"] = recipient

    # Plain-text version
    message.set_content(body)

    # HTML version, with plain text retained as a fallback
    if html_body:
        message.add_alternative(html_body, subtype="html")

    try:
        with smtplib.SMTP(
            "smtp.gmail.com", 587, timeout=30
        ) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            smtp.send_message(message)

        print(f"Email sent successfully to {recipient}")

    except (smtplib.SMTPException, OSError) as error:
        print(f"Failed to send email: {error}")
        raise
