
import os
import smtplib
import streamlit as st
from email.message import EmailMessage
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

# Get email credentials
try:
    EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]

except Exception:
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_otp_email(receiver_email, otp):

    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email credentials are missing.")
        return False

    msg = EmailMessage()

    msg["Subject"] = "SecureLogin - OTP Verification"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    msg.set_content(
        f"Your SecureLogin verification code is: {otp}\n\n"
        "Please do not share this code with anyone.\n\n"
        "Thank you for using SecureLogin!"
    )

    try:
        server = smtplib.SMTP(
            "smtp.gmail.com",
            587,
            timeout=20
        )

        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print("Email sending failed:", repr(e))

        return False
