from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action
import requests
import logging
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

logger = logging.getLogger(__name__)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            logger.error("Error fetching products", exc_info=True)
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=False, methods=['get'], url_path='get-or-create')
    def get_or_create_cart(self, request):
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = self._create_new_cart(request)
        else:
            cart = self._create_new_cart(request)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    def _create_new_cart(self, request):
        cart = Cart.objects.create(auth0_user_id='anonymous')
        request.session['cart_id'] = cart.id
        return cart

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        logger.debug(f"Received data: {request.data}")

        cart_id = request.data.get('cart')
        if not cart_id:
            return Response({"error": "Cart ID is not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['cart'] = cart.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Store API!"})

class UserRolesView(APIView):
    def get(self, request, user_id):
        try:
            roles = get_user_roles(user_id)
            return JsonResponse({'user_id': user_id, 'roles': roles})
        except requests.HTTPError as e:
            return JsonResponse({'error': str(e)}, status=e.response.status_code)