import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

class EmailSender:
    def __init__(self, settings_model):
        self.settings = settings_model
        
    def send_report(self, subject, body, attachment_path=None):
        sender_email = self.settings.get("email_sender")
        sender_password = self.settings.get("email_password")
        recipient_email = self.settings.get("email_recipient")
        
        if not sender_email or not sender_password or not recipient_email:
            print("Email settings incomplete.")
            return False, "Email settings incomplete"
            
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            if attachment_path and os.path.exists(attachment_path):
                attachment = open(attachment_path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
                msg.attach(part)
                
            # SMTP Setup (Gmail default)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            
            return True, "Email sent successfully"
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False, str(e)
