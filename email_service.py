
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")



def send_otp_email(receiver_email, otp):
    msg = EmailMessage()
    msg["Subject"] = "SecureLogin - OTP Verification"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = receiver_email

    msg.set_content(
        f"Your SecureLogin verification code is: {otp}\n"
        "Please do not share this code with anyone."
    )

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        

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
