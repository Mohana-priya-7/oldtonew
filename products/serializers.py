from rest_framework import serializers 
from .models import Product 
from django.contrib.auth.models import User
from products.utils import validate_strong_password
class ProductSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'})   
    class Meta:
        model=User
        fields=('username','email','password','password2')
        extra_kwargs={'email':{'required':True}}
        def validate_password(self, data):
            return validate_strong_password(data)
        def validate(self, data):   
            if data['password']!= data['password2']:
                raise serializers.ValidationError("Passwords do not match.")
            return data
        def create(self, validated_data):   
            validated_data.pop('password2')
            user=User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user