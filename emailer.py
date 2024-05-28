import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

def send(string):
    load_dotenv()
    # Email variables
    sender_email = os.getenv("USERNAME_GMAIL")
    receiver_email = os.getenv("RECEIVER")
    password = os.getenv("PASSWORD_GMAIL")  # Use the app password you generated

    # Create the email object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Neue Note in HISQIS"

    # Add the email body
    body = string
    message.attach(MIMEText(body, "plain"))

    # Gmail SMTP server setup
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls

    # Create a secure SSL context and send the email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()