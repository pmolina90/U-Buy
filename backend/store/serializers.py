from rest_framework import serializers
from rest_framework.permissions import AllowAny
from decimal import Decimal
from .models import Category, Product, Cart, CartItem, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        permission_classes = [AllowAny]
        
class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'))
    
    class Meta:
        model = Product
        fields = '__all__'
        permission_classes = [AllowAny]
        
class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity']
        permission_classes = [AllowAny]
        
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Include CartItems in the Cart representation
    
    class Meta:
        model = Cart
        fields = ['id', 'auth0_user_id', 'items', 'created_at', 'updated_at']
        permission_classes = [AllowAny]
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        permission_classes = [AllowAny]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        permission_classes = [AllowAny]