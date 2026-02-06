import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, Category
from blog.models import Post, Author

class Command(BaseCommand):
    help = 'Load mockup data for Products and Blog from JSON files'

    def handle(self, *args, **kwargs):
        # เรียกใช้ฟังก์ชันย่อย
        self.seed_products()
        self.seed_blog()
        self.stdout.write(self.style.SUCCESS('\nAll data seeded successfully! 🚀'))

    def seed_products(self):
        # 1. ระบุตำแหน่งไฟล์
        file_path = os.path.join(settings.BASE_DIR, 'products', 'fixtures', 'products_data.json')
        self.stdout.write(f'Loading Products from {file_path}...')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('Product file not found!'))
            return

        # 2. อ่านไฟล์ JSON
        with open(file_path, 'r', encoding='utf-8') as file:
            categories_data = json.load(file)

        # 3. วนลูปบันทึกข้อมูล
        for cat_data in categories_data:
            # สร้าง Category
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'], # ใช้ slug เป็นตัวเช็คว่ามีอยู่แล้วหรือยัง
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'image': cat_data['image']
                }
            )
            
            # สร้าง Products ใน Category นั้น
            for prod_data in cat_data['products']:
                Product.objects.get_or_create(
                    slug=prod_data['slug'],
                    defaults={
                        'category': category,
                        'name': prod_data['name'],
                        'description': prod_data['description'],
                        'body': prod_data['body'],
                        'price': prod_data['price'],
                        'available': prod_data['available'],
                        'image': prod_data['image']
                    }
                )

    def seed_blog(self):
        file_path = os.path.join(settings.BASE_DIR, 'blog', 'fixtures', 'blog_data.json')
        self.stdout.write(f'\nLoading Blog from {file_path}...')

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('Blog file not found!'))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            authors_data = json.load(file)

        for auth_data in authors_data:
            # สร้าง Author
            author, created = Author.objects.get_or_create(
                email=auth_data['email'],
                defaults={
                    'name': auth_data['name'],
                    'bio': auth_data['bio'],
                    'profile_picture': auth_data['profile_picture']
                }
            )

            # สร้าง Posts ของ Author นั้น
            for post_data in auth_data['posts']:
                Post.objects.get_or_create(
                    slug=post_data['slug'],
                    defaults={
                        'author': author,
                        'title': post_data['title'],
                        'description': post_data['description'],
                        'body': post_data['body'],
                        'featured_image': post_data['featured_image']
                    }
                )
