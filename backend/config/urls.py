from django.contrib import admin
from django.urls import path, include

try:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
    print("Successfully imported JWT views")
except ImportError as e:
    print(f"Error importing JWT views: {e}")
    sys.exit(1)  # Exit the program if the import fails

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('api/v1/', include('store.urls')),  # Version 1
    # path('api/v2/', include('store_v2.urls')),  # Future version
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]