from rest_framework import serializers 
from .models import Product 
from django.contrib.auth import get_user_model
from products.utils import validate_strong_password
User = get_user_model()

#Nested serializers are used to represent related objects inside a single API response, improving API usability and reducing extra requests.
#Nested serializers allow you to include related objects within the same API response. This is useful for representing complex relationships between models in a single API call, reducing the need for multiple requests to fetch related data.    
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email') 

class ProductSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_by=UserMiniSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at','created_by']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_strong_password],style={'input_type':'password'})
    class Meta:
        model=User
        fields=('username','email','password')
        extra_kwargs={'email':{'required':True}}
    def create(self, validated_data):
        user=User(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
#Nested serializers allow you to include related objects within the same API response. This is useful for representing complex relationships between models in a single API call, reducing the need for multiple requests to fetch related data.    
class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email')