from django.urls import path
from .views import EmailTokenObtainPairView
urlpatterns = [
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),] 