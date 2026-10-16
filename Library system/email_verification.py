import os
import secrets
import smtplib
import time
from email.message import EmailMessage

SENDER_EMAIL = os.getenv("LIBRARY_GMAIL_ADDRESS")
APP_PASSWORD = os.getenv("LIBRARY_GMAIL_APP_PASSWORD")


def verify_email(recipient_email):
    if not SENDER_EMAIL or not APP_PASSWORD:
        print("Email server configuration is missing.")
        return False

    verification_code = f"{secrets.randbelow(1_000_000):06d}"

    message = EmailMessage()
    message["Subject"] = "Library System - Email Verification"
    message["From"] = SENDER_EMAIL
    message["To"] = recipient_email

    message.set_content(
        f"Your verification code is: {verification_code}\n\n"
        "This code expires in 120 seconds."
    )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            result = server.send_message(message)

            if result:
                print(f"Email rejected by recipient server: {result}")
            else:
                print(f"Email accepted for delivery to {recipient_email}.")

        print(f"A verification code has been sent to {recipient_email}.")

    except (OSError, smtplib.SMTPException) as error:
        print(f"Email sending failed: {type(error).__name__}")
        return False

    expires_at = time.monotonic() + 120

    for attempt in range(3):
        if time.monotonic() >= expires_at:
            print("Verification code expired.")
            return False

        entered_code = input("Enter the verification code: ").strip()

        if time.monotonic() >= expires_at:
            print("Verification code expired.")
            return False

        if entered_code == verification_code:
            print("Email verified successfully.")
            return True

        if attempt < 2:
            print(f"Incorrect code. Attempts remaining: {2 - attempt}")

    print("Too many incorrect attempts.")
    return False


if __name__ == "__main__":
    recipient = input(
        "Enter the email to verify: "
    ).strip().lower()

    if verify_email(recipient):
        print("TEST PASSED: Email verification successful.")
    else:
        print("TEST FAILED: Email was not verified.")
