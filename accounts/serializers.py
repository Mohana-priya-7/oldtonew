from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.utils import validate_strong_password
User = get_user_model()
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD 
    """Configures the serializer to accept email instead of username for login"""
    """Sets email as the primary login field instead of username"""
    """DRF's TokenObtainPairSerializer for JWT authentication"""

class ChangePasswordSerializer(serializers.Serializer): 
    old_password = serializers.CharField(write_only=True, style={'input_type':'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type':'password'},validators=[validate_strong_password])    
    def validate_new_password(self, value):
        return validate_strong_password(value)   
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True)
    def validate_new_password(self, value):
        return validate_strong_password(value) 