import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

PORT = 465
SMTP_SERVER = "smtp.gmail.com"
context = ssl.create_default_context()

class Send_message:
    def __init__(self, receiver_email, receiver_name, sender_email, sender_pass):
        self.receiver_email = receiver_email
        self.receiver_name = receiver_name
        self.sender_email = sender_email
        self.sender_pass = sender_pass

    def send(self, subject="Welcome to the Phone Book 📱", body="Hello {name},\n\nYou’ve been added to a digital phone book.\n\nBest regards,\nAli's Python CLI App"):
        body = body.replace("{name}", self.receiver_name)

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, port=PORT, context=context) as server:
                server.login(self.sender_email, self.sender_pass)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            print("📧 Email sent to contact successfully.")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
