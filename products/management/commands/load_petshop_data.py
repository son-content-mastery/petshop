import json
import os
from django.core.management.base import BaseCommand
from products.models import Category, Product

class Command(BaseCommand):
    help = 'Load mockup data from products_data.json'

    def handle(self, *args, **options):
        # Path to the JSON file relative to manage.py
        file_path = os.path.join('products', 'fixtures', 'products_data.json')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} not found.'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for cat_data in data:
            # Create or update category
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data.get('description', ''),
                    'image': cat_data.get('image', '')
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(f"Updated category: {category.name}")

            # Create or update products in this category
            for prod_data in cat_data.get('products', []):
                product, created = Product.objects.update_or_create(
                    slug=prod_data['slug'],
                    defaults={
                        'category': category,
                        'name': prod_data['name'],
                        'description': prod_data.get('description', ''),
                        'body': prod_data.get('body', ''),
                        'price': prod_data['price'],
                        'available': prod_data.get('available', True),
                        'image': prod_data.get('image', '')
                    }
                )
                
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  - Created product: {product.name}"))
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded mockup data.'))
