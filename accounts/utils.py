from datetime import timedelta
from django.utils import timezone
from django.conf import settings 
import random,string 
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from accounts import serializers 
def generate_otp():
    """Generates a 6-digit numeric OTP"""
    otp=''.join(random.choices(string.digits,k=6))
    return otp 

def validate_strong_password(password):
    if len(password)<8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one digit.")
    if not any(char in '@#$%^&*' for char in password):
        raise ValidationError("Password must contain at least one special character (@#$%^&*).")
    return password
def send_otp_via_email(email, otp):
    try:
        subject = 'Your OTP Code'
        message = f'Your OTP is: {otp}'
        email_from = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 
def is_otp_valid(otp_created_time, expiry_minutes=10):
    """Checks if the entered OTP matches the user's OTP"""
    if not otp_created_time:
        return False   
    current_time = timezone.now()
    otp_expiry_time = otp_created_time + timedelta(minutes=expiry_minutes)
    return current_time <= otp_expiry_time
"""This is a QUESTION, not a statement.
It is asking:
It is asking:
❓ “Is the current time LESS THAN or EQUAL TO the expiry time?”"""