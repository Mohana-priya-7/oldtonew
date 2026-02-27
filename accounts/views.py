from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainPairSerializer,ChangePasswordSerializer,ForgotPasswordSerializer, User,ResetPasswordSerializer,VerifyOTPSerializer
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ForgetPassword
from accounts.tasks import send_otp_email 
from django.core.cache import cache 
import random
from .throttles import OTPThrottle
from accounts.utils import is_otp_valid
from drf_spectacular.utils import extend_schema

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        request=ChangePasswordSerializer, 
        responses={200: dict, 400: dict})
    def put(self, request):
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
    throttle_classes = [OTPThrottle]  #Apply OTPThrottle to this view
    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: dict, 400: dict}
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].strip().lower()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=400)
            otp = str(random.randint(100000, 999999))
            #Store in Redis (performance)
            cache.set(f"otp:{email}",otp,timeout=300) #5 min
            #Store in DB (audit / record)
            ForgetPassword.objects.create(user=user,otp=otp)         
            send_otp_email.delay(email,otp)
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
        email=request.data.get("email").strip().lower()
        entered_otp=serializer.validated_data['otp']
        
        #Get OTP from Redis
        stored_otp=cache.get(f"otp:{email}")
        if not stored_otp:
            return Response({"Error":"OTP expired or not found"},status=status.HTTP_400_BAD_REQUEST)
        if stored_otp!=entered_otp:
            return Response({"Error":"Invalid OTP"},status=status.HTTP_400_BAD_REQUEST)
        otp_obj = ForgetPassword.objects.filter(
            user__email=email,
            otp=entered_otp,
            is_used=False
        ).order_by('-created_at').first()

        if otp_obj:
            otp_obj.is_used = True
            otp_obj.save()

        # 4️⃣ Delete OTP from Redis
        cache.delete(f"otp:{email}")

        return Response(
            {"message": "OTP verified successfully"},
            status=status.HTTP_200_OK
        )


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
            return Response({"error": "Invalid or already used OTP"},status=status.HTTP_400_BAD_REQUEST)
        # ✅ OTP expiry check (good practice)
        if not is_otp_valid(otp_obj.created_at):return Response({"error": "OTP expired"},status=status.HTTP_400_BAD_REQUEST)
        user = otp_obj.user
        user.set_password(new_password)
        user.save()
        # 🔥 STEP 4 IS HERE (THIS IS THE ANSWER)
        otp_obj.is_used = True
        otp_obj.save() 
        return Response({"message": "Password reset successfully"},status=status.HTTP_200_OK)