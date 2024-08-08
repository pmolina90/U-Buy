from django.test import TestCase
from decimal import Decimal
from store.models import Category, Product, Cart, CartItem, Order, OrderItem
from store.serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer

class CategorySerializerTest(TestCase):
    def setUp(self):
        self.category_data = {'name': 'XXX23', 'image': 'https://via.placeholder.com/150'}
        self.category = Category.objects.create(**self.category_data)
        self.serializer = CategorySerializer(instance=self.category)
    
    def tearDown(self):
        Category.objects.all().delete()

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'image', 'created_at', 'updated_at']))

    def test_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['name'], self.category_data['name'])

    def test_image_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['image'], self.category_data['image'])

    def test_create_category(self):
        new_category_data = {'name': 'caca2', 'image': 'https://via.placeholder.com/150'}
        serializer = CategorySerializer(data=new_category_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()
        self.assertEqual(category.name, new_category_data['name'])
        self.assertEqual(category.image, new_category_data['image'])

class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='https://via.placeholder.com/150')
        self.product_data = {
            'title': 'Smartphone',
            'name': 'iPhone',
            'price': '999.99',
            'description': 'Latest model',
            'stock': 10,
            'images': {'front': '', 'back': ''},
            'category': self.category.id
        }
        self.product = Product.objects.create(
            title=self.product_data['title'],
            name=self.product_data['name'],
            price=Decimal(self.product_data['price']),
            description=self.product_data['description'],
            stock=self.product_data['stock'],
            images=self.product_data['images'],
            category=self.category
        )
        self.serializer = ProductSerializer(instance=self.product)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'title', 'name', 'price', 'description', 'stock', 'images', 'category', 'created_at', 'updated_at']))

    def test_title_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['title'], self.product_data['title'])

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], str(self.product_data['price']))

    def test_create_product(self):
        serializer = ProductSerializer(data=self.product_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.title, self.product_data['title'])
        self.assertEqual(product.price, Decimal(self.product_data['price']))

class CartSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='https://via.placeholder.com/150')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart_data = {'auth0_user_id': 'auth0|123456', 'products': [self.product.id]}
        self.cart = Cart.objects.create(auth0_user_id='auth0|123456')
        self.serializer = CartSerializer(instance=self.cart)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'auth0_user_id', 'created_at', 'updated_at', 'products']))

    def test_auth0_user_id_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['auth0_user_id'], self.cart_data['auth0_user_id'])

    def test_create_cart(self):
        serializer = CartSerializer(data=self.cart_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        cart = serializer.save()
        self.assertEqual(cart.auth0_user_id, self.cart_data['auth0_user_id'])

class CartItemSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='https://via.placeholder.com/150')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart = Cart.objects.create(auth0_user_id='auth0|123456')
        self.cart_item_data = {'cart': self.cart.id, 'product': self.product.id, 'quantity': 2}
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.serializer = CartItemSerializer(instance=self.cart_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'cart', 'product', 'quantity']))

    def test_quantity_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['quantity'], self.cart_item_data['quantity'])

    def test_create_cart_item(self):
        serializer = CartItemSerializer(data=self.cart_item_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        cart_item = serializer.save()
        self.assertEqual(cart_item.quantity, self.cart_item_data['quantity'])

class OrderSerializerTest(TestCase):
    def setUp(self):
        self.order_data = {'auth0_user_id': 'auth0|123456', 'total_amount': '1999.98'}
        self.order = Order.objects.create(**self.order_data)
        self.serializer = OrderSerializer(instance=self.order)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'auth0_user_id', 'total_amount', 'created_at', 'updated_at']))

    def test_total_amount_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['total_amount'], self.order_data['total_amount'])

    def test_create_order(self):
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.total_amount, Decimal(self.order_data['total_amount']))

class OrderItemSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='https://via.placeholder.com/150')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=Decimal('999.99'),
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.order = Order.objects.create(auth0_user_id='auth0|123456', total_amount=Decimal('1999.98'))
        self.order_item_data = {'order': self.order.id, 'product': self.product.id, 'quantity': 2, 'price': '999.99'}
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=Decimal('999.99'))
        self.serializer = OrderItemSerializer(instance=self.order_item)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'order', 'product', 'quantity', 'price']))

    def test_quantity_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['quantity'], self.order_item_data['quantity'])

    def test_price_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['price'], self.order_item_data['price'])

    def test_create_order_item(self):
        serializer = OrderItemSerializer(data=self.order_item_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order_item = serializer.save()
        self.assertEqual(order_item.quantity, self.order_item_data['quantity'])
        self.assertEqual(order_item.price, Decimal(self.order_item_data['price']))