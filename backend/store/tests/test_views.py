from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from decimal import Decimal
from store.models import Category, Product, Cart, CartItem, Order, OrderItem
from store.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer


class BaseTestCase(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        # Obtain JWT token
        self.token = self.get_token()
        
        # Set the Authorization header for all subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_token(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        return response.data['access']

class CategoryViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Electronics', image='')
        self.url = reverse('category-list')

    def test_get_categories(self):
        response = self.client.get(self.url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_category(self):
        data = {'name': 'Books', 'image': 'https://via.placeholder.com/150'}  # Provide a non-blank value for 'image'
        response = self.client.post(self.url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Category creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(id=2).name, 'Books')

class ProductViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.url = reverse('product-list')

    def test_get_products(self):
        response = self.client.get(self.url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_product(self):
        data = {
            'title': 'Tablet',
            'name': 'iPad',
            'price': '499.99',
            'description': 'New model',
            'stock': 5,
            'images': {'front': '', 'back': ''},
            'category': self.category.id
        }
        response = self.client.post(self.url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Product creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=2).name, 'iPad')

class CartViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Electronics', image='some_image_url.jpg')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart = Cart.objects.create(auth0_user_id=self.user.id)
        self.url = reverse('cart-list')

    def test_get_carts(self):
        response = self.client.get(self.url)
        carts = Cart.objects.all()
        serializer = CartSerializer(carts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cart(self):
        data = {
            'auth0_user_id': str(self.user.id),
            'products': [self.product.id]  # Ensure 'products' is provided, even if empty
        }
        response = self.client.post(self.url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Cart creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 2)
        self.assertEqual(Cart.objects.get(id=2).auth0_user_id, str(self.user.id))

class CartItemViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart = Cart.objects.create(auth0_user_id=self.user.id)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.url = reverse('cartitem-list')

    def test_get_cart_items(self):
        response = self.client.get(self.url)
        cart_items = CartItem.objects.all()
        serializer = CartItemSerializer(cart_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_cart_item(self):
        data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 3}
        response = self.client.post(self.url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"CartItem creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 2)
        self.assertEqual(CartItem.objects.get(id=2).quantity, 3)

class OrderViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.order = Order.objects.create(auth0_user_id=self.user.id, total_amount=Decimal('1999.98'))
        self.url = reverse('order-list')

    def test_get_orders(self):
        response = self.client.get(self.url)
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        data = {'auth0_user_id': str(self.user.id), 'total_amount': '999.99'}
        response = self.client.post(self.url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Order creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=2).total_amount, Decimal('999.99'))

class OrderItemViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.order = Order.objects.create(auth0_user_id=self.user.id, total_amount=Decimal('1999.98'))
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('999.99'))
        self.url = reverse('orderitem-list')

    def test_get_order_items(self):
        response = self.client.get(self.url)
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_order_item(self):
        data = {'order': self.order.id, 'product': self.product.id, 'quantity': 1, 'price': '499.99'}
        response = self.client.post(self.url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print(f"OrderItem creation failed: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderItem.objects.count(), 2)
        self.assertEqual(OrderItem.objects.get(id=2).quantity, 1)
        self.assertEqual(OrderItem.objects.get(id=2).price, Decimal('499.99'))

class HomeViewTest(APITestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')