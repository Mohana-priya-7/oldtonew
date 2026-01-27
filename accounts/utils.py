from datetime import timedelta,datetime
from django.conf import settings 
import random,string 
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import serializers

from accounts import serializers 
def generate_otp():
    """Generates a 6-digit numeric OTP"""
    otp=''.join(random.choices(string.digits,k=6))
    return otp 

def validate_strong_password(password):
    if len(password)<8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not any(char.isupper() for char in password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not any(char.islower() for char in password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not any(char.isdigit() for char in password):
        raise serializers.ValidationError("Password must contain at least one digit.")
    if not any(char in '@#$%^&*' for char in password):
        raise serializers.ValidationError("Password must contain at least one special character (@#$%^&*).")
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
def is_otp_valid(otp_created_time):
    """Checks if the entered OTP matches the user's OTP"""
    if otp_created_time is None:
        return False   
    return True
    current_time = datetime.now() 
    time_difference = current_time - otp_created_time
    if time_difference.total_seconds()>120:
        return True  # Expired
    else:
        return False  # Still valid