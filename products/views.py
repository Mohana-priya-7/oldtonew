from .models import Product
from .serializers import ProductSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from drf_spectacular.utils import extend_schema 
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import get_user_model
User = get_user_model()
class ProductList(APIView):
    @extend_schema(
            responses=ProductSerializer(many=True)
    )
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data) 
    
    @extend_schema(
        request=ProductSerializer,
        responses=ProductSerializer
    ) 
    def post(self,request):
        serializer =ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserRegistration(APIView):
    permission_classes=[AllowAny]
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer,400: None}
    )
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User registered successfully.',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)