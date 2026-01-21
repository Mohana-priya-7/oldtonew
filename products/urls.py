from django.urls import path
from .views import ProductList,UserRegistration
urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('register/', UserRegistration.as_view(), name='user-registration'),
]                                                                