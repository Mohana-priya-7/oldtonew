from rest_framework import serializers 
from .models import Product 
class ProductSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at']