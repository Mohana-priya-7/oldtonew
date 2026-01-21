from .models import Product
from .serializers import ProductSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView 
from drf_spectacular.utils import extend_schema 
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