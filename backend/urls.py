from django.urls import path,include
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView 
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from django.contrib import admin
urlpatterns = [
    path('', include('products.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('swagger/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('admin/',admin.site.urls)] 