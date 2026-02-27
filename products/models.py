from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
class Product(models.Model):
    name=models.CharField(max_length=100,unique=True)
    price=models.IntegerField()
    description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)      
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="products")
    
    #One user can create many products.This relationship is required for nested serializers.related_name="products" allows reverse access
    #The reverse axis means accessing the related objects from the OTHER side of the relationship.

    def __str__(self):
        return self.name