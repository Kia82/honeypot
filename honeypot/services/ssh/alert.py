import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from enum import Enum
load_dotenv()


class Service(Enum):
    SSH="SSH"
    HTTP="HTTP"
    FTP="FTP"

def send_email_alert(ip, service: Service):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    subject = "⚠️ Honeypot Alert"
    body = f"A connection was made from IP: {ip}. Threat actor connected to the {service} service"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("[+] Alert email sent.")
    except Exception as e:
        print(f"[-] Failed to send alert email: {e}")
