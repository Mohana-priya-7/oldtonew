#serializers means: Translator between Django models and JSON

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#TokenObtainPairSerializer?It is a built-in serializer that:Accepts login credentials,Validates user,Returns two tokens:refresh,access

from django.contrib.auth import get_user_model
#Import function to get active user model

from rest_framework import serializers
from accounts.utils import validate_strong_password,is_otp_valid
from accounts.models import ForgetPassword
User = get_user_model()
#Assign active user model to User variable

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD 
    """Configures the serializer to accept email instead of username for login"""
    """Sets email as the primary login field instead of username"""
    """DRF's TokenObtainPairSerializer for JWT authentication"""

class ChangePasswordSerializer(serializers.Serializer): 
    old_password = serializers.CharField(write_only=True, style={'input_type':'password'})
    new_password = serializers.CharField(write_only=True, style={'input_type':'password'},validators=[validate_strong_password])    
    def validate_new_password(self, value): #def validate_password(self, value): checks one filed in isolation 
        return validate_strong_password(value)   
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class VerifyOTPSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp = serializers.CharField(max_length=6, required=True)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(write_only=True)
    def validate_new_password(self, value):
        return validate_strong_password(value) 
    #object-level validation to check if the provided OTP is valid for the given email and not expired
    def validate(self, data):
        otp_obj = ForgetPassword.objects.filter(
            user__email=data['email'],
            otp=data['otp'],
            is_used=False
        ).first()
#Returns first matching object.If nothing matches → returns None.Avoids exceptions like .get() would raise

        if not otp_obj: #If otp_obj is None ,i.e., no matching record found in DB
            raise serializers.ValidationError("Invalid email or OTP")
        if not is_otp_valid(otp_obj.created_at):
            raise serializers.ValidationError("OTP expired")
        data['otp_obj'] = otp_obj
        return data