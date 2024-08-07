from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)  # Name of the category, Ensuring the name is unique
    image = models.URLField()  # URL of the category image (To make optional use "blank=True, null=True")
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update
    
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255, default='Default Title')  # Title of the product
    name = models.CharField(max_length=255, db_index=True)  # Name of the product
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)], db_index=True)  # Price of the product
    description = models.TextField()  # Description of the product
    stock = models.PositiveBigIntegerField(db_index=True)  # Stock of the product
    images = models.JSONField()  # JSON field to store images
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, db_index=True)  # Category of the product
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update
    
    objects = models.Manager()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    auth0_user_id = models.CharField(max_length=255, db_index=True)  # Auth0 user ID
    products = models.ManyToManyField(Product)  # Products in the cart
    created_at = models.DateTimeField(auto_now_add=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update
    
    def __str__(self):
        return f'Cart {self.id} for {self.auth0_user_id}'
        
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)  # Cart that the item belongs to
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product in the cart item
    quantity = models.PositiveBigIntegerField()  # Quantity of the product in the cart
    
    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart {self.cart.id}'
    
class Order(models.Model):
    auth0_user_id = models.CharField(max_length=255, db_index=True)  # Auth0 user ID
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)  # Date and time of creation
    updated_at = models.DateTimeField(auto_now=True)  # Date and time of last update
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)], db_index=True)  # Total amount of the order
    
    def __str__(self):
        return f'Order {self.id} for {self.auth0_user_id}'    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # Order that the item belongs to
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product in the order item
    quantity = models.PositiveBigIntegerField()  # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])  # Price of the product
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name} at {self.price} each'