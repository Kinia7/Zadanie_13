import os
import smtplib
from email.mime.text import MIMEText
from flask import url_for
from itsdangerous import URLSafeTimedSerializer

def send_verification_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = f'<p>Proszę kliknąć na poniższy link, aby potwierdzić adres email:</p><p><a href="{confirm_url}">{confirm_url}</a></p>'
    subject = "Potwierdzenie adresu email"
    
    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['From'] = os.getenv('MAIL_USERNAME')
    msg['To'] = user_email
    
    with smtplib.SMTP(os.getenv('MAIL_SERVER'), os.getenv('MAIL_PORT')) as server:
        server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        server.send_message(msg)

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    return serializer.dumps(email, salt=os.getenv('SECURITY_PASSWORD_SALT'))

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
    try:
        email = serializer.loads(token, salt=os.getenv('SECURITY_PASSWORD_SALT'), max_age=expiration)
    except:
        return False
    return email
