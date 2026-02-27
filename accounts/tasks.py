from celery import shared_task
from django.core.mail import send_mail 
from django.conf import settings 
from django.utils import timezone
from datetime import timedelta
from accounts.models import CustomUser 
@shared_task

#“This function is a background task.Do NOT run it in Django request cycle.Run it using a Celery worker.”

def send_otp_email(email,otp):
    print("Celery is executed") 
    send_mail(
        subject="Password Reset otp",
        message=f"Your OTP for password reset is:{otp} ",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False, 
    )

@shared_task
def user_regis_report():
    y=timezone.now()-timedelta(days=1)
    ct=CustomUser.objects.filter(date_joined__gte=y).count()
    #Count how many users registered in the last 24 hours
    send_mail(
        subject="Daily User Registration Report",
        message=f"{ct} Users Registered in last 24 hours.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["s.mohanapriya2174@gmail.com"],
        fail_silently=False,
    )