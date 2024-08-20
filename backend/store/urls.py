from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartViewSet, CartItemViewSet, OrderViewSet, OrderItemViewSet, HomeView, UserRolesView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('api/v1/', include(router.urls)),
    path('api/v1/cart/get-or-create/', CartViewSet.as_view({'get': 'get_or_create_cart'}), name='get-or-create-cart'),  
    path('api/user-roles/<str:user_id>/', UserRolesView.as_view(), name='user-roles'),
]

