from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer,ChangePasswordSerializer,ForgotPasswordSerializer, User,ResetPasswordSerializer,VerifyOTPSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ForgetPassword
import random
from django.contrib.auth import get_user_model
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
        user = request.user
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            if not user.check_password(old_password):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgePasswordView(APIView):
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
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_obj = ForgetPassword.objects.filter(user=user, otp=otp, is_used=False).last()
                if not otp_obj:
                    return Response({"error": "Invalid OTP"}, status=400)
                return Response({"message": "OTP verified successfully"}, status=200)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=400)
        return Response(serializer.errors, status=400)
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                otp_obj = ForgetPassword.objects.filter(user=user, otp=otp, is_used=False).last()
                if not otp_obj:
                    return Response({"error": "Invalid OTP"}, status=400)
                user.set_password(new_password)
                user.save()
                otp_obj.is_used = True
                otp_obj.save()
                return Response({"message": "Password reset successfully"}, status=200)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=400)
        return Response(serializer.errors, status=400)