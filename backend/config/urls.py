import sys


from django.contrib import admin
from django.urls import path, include

try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
except ImportError as e:
    print(f"Error import JWT views: {e}")    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
