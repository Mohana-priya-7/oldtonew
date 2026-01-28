from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser 
class CustomUser(AbstractUser):
    username=models.CharField(max_length=20)
    email=models.EmailField(unique=True)
    otp=models.CharField(max_length=6,blank=True,null=True)
    verified=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

class ForgetPassword(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    """ This allows the ForgetPassword model to track which user requested a password reset. The CASCADE behavior ensures no orphaned records remain if a user account is removed."""
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now) 
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username} - {self.otp}"