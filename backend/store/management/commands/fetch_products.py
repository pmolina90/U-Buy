import requests
from django.core.management.base import BaseCommand
from store.models import Category, Product

class Command(BaseCommand):
    help ='Fetch products from API and save to database'
    
    def handle(self, *args, **kwargs):
        url = 'https://api.escuelajs.co/api/v1/products'
        response = requests.get(url)
        products = response.json()
        
        for product in products:
            category_data = product['category']
            category, created = Category.objects.update_or_create(
                id=category_data['id'],
                defaults={
                    'name': category_data['name'],
                    'image': category_data['image'],
                }
            )
            
            Product.objects.update_or_create(
                id=product['id'],
                defaults={
                    'title': product['title'],
                    'name': product['title'],
                    'price': product['price'],
                    'description': product['description'],
                    'images': product['images'],
                    'created_at': product['creationAt'],
                    'updated_at': product['updatedAt'],
                    'category': category,
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved products'))                