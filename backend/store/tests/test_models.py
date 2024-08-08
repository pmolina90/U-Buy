from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from store.models import Category, Product, Cart, CartItem, Order, OrderItem


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.image, '')
        self.assertIsInstance(self.category.created_at, timezone.datetime)
        self.assertIsInstance(self.category.updated_at, timezone.datetime)

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=999.99,
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.title, 'Smartphone')
        self.assertEqual(self.product.name, 'iPhone')
        self.assertEqual(self.product.price, 999.99)
        self.assertEqual(self.product.description, 'Latest model')
        self.assertEqual(self.product.stock, 10)
        self.assertEqual(self.product.images['front'], '')
        self.assertEqual(self.product.category.name, 'Electronics')
        self.assertIsInstance(self.product.created_at, timezone.datetime)
        self.assertIsInstance(self.product.updated_at, timezone.datetime)

    def test_product_price_validation(self):
        with self.assertRaises(ValidationError):
            product = Product(
                title='Smartphone',
                name='iPhone',
                price=-1.00,  # Invalid price
                description='Latest model',
                stock=10,
                images={'front': '', 'back': ''},
                category=self.category
            )
            product.full_clean()  # This will trigger the validation

class CartModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=999.99,
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart = Cart.objects.create(auth0_user_id='user123')

    def test_cart_creation(self):
        self.assertEqual(self.cart.auth0_user_id, 'user123')
        self.assertIsInstance(self.cart.created_at, timezone.datetime)
        self.assertIsInstance(self.cart.updated_at, timezone.datetime)

    def test_cart_add_product(self):
        self.cart.products.add(self.product)
        self.assertIn(self.product, self.cart.products.all())
        
class CartItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=999.99,
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.cart = Cart.objects.create(auth0_user_id='user123')
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

class OrderModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=999.99,
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.order = Order.objects.create(auth0_user_id='user123', total_amount=1999.98)

    def test_order_creation(self):
        self.assertEqual(self.order.auth0_user_id, 'user123')
        self.assertEqual(self.order.total_amount, 1999.98)
        self.assertIsInstance(self.order.created_at, timezone.datetime)
        self.assertIsInstance(self.order.updated_at, timezone.datetime)

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', image='')
        self.product = Product.objects.create(
            title='Smartphone',
            name='iPhone',
            price=999.99,
            description='Latest model',
            stock=10,
            images={'front': '', 'back': ''},
            category=self.category
        )
        self.order = Order.objects.create(auth0_user_id='user123', total_amount=1999.98)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2, price=999.99)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 999.99)        