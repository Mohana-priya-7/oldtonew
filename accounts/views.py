from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer,ChangePasswordSerializer,ForgotPasswordSerializer, User,ResetPasswordSerializer,VerifyOTPSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ForgetPassword
import random
from accounts.utils import is_otp_valid
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ChangePasswordSerializer, 
        responses={200: dict, 400: dict})
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return Response({"error": "New password cannot be the same as the old password"}, status=status.HTTP_400_BAD_REQUEST) 
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)

class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=400)
            otp = str(random.randint(100000, 999999))
            ForgetPassword.objects.create(
                user=user,
                otp=otp
            )
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp}",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to email successfully"}, status=200)
        return Response(serializer.errors, status=400)
    
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=VerifyOTPSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        otp_obj = ForgetPassword.objects.filter(otp=otp, is_used=False).order_by('-created_at').first()
        if not otp_obj:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        """ Check if OTP is expired """
        if not is_otp_valid(otp_obj.created_at, expiry_minutes=10):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']
        otp_obj = ForgetPassword.objects.filter(
            otp=otp,
            is_used=False
        ).order_by('-created_at').first()
        if not otp_obj:
            return Response(
                {"error": "Invalid or already used OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # ✅ OTP expiry check (good practice)
        if not is_otp_valid(otp_obj.created_at):
            return Response(
                {"error": "OTP expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user = otp_obj.user
        user.set_password(new_password)
        user.save()
        # 🔥 STEP 4 IS HERE (THIS IS THE ANSWER)
        otp_obj.is_used = True
        otp_obj.save()
        return Response(
            {"message": "Password reset successfully"},
            status=status.HTTP_200_OK
        )