import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError

from blog.models import Author, Post
from products.models import Category, Product


class Command(BaseCommand):
    help = 'Create or update the reusable product and blog seed data.'
    legacy_post_slugs = [
        'why-cats-love-boxes',
        'wet-vs-dry-food',
        'cat-vaccination-schedule',
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-images',
            action='store_true',
            help='Seed database records without downloading remote images.',
        )
        parser.add_argument(
            '--refresh-images',
            action='store_true',
            help='Download remote images again even when an image already exists.',
        )

    def handle(self, *args, **options):
        self.skip_images = options['skip_images']
        self.refresh_images = options['refresh_images']
        self.image_cache = {}
        self.seed_products()
        self.seed_blog()
        self.stdout.write(self.style.SUCCESS('Product and blog seed data is ready.'))

    def load_json(self, relative_path):
        file_path = Path(settings.BASE_DIR) / relative_path
        try:
            with file_path.open(encoding='utf-8') as fixture:
                return json.load(fixture)
        except (OSError, json.JSONDecodeError) as exc:
            raise CommandError(f'Could not load {file_path}: {exc}') from exc

    def seed_products(self):
        data = self.load_json('products/fixtures/products_data.json')

        for category_data in data:
            category, _ = Category.objects.update_or_create(
                slug=category_data['slug'],
                defaults={
                    'name': category_data['name'],
                    'description': category_data.get('description', ''),
                    'image': category_data.get('image', ''),
                },
            )
            for product_data in category_data.get('products', []):
                defaults = {
                    'category': category,
                    'name': product_data['name'],
                    'description': product_data.get('description', ''),
                    'body': product_data.get('body', ''),
                    'price': product_data['price'],
                    'available': product_data.get('available', True),
                    'image_alt': product_data.get('image_alt', ''),
                    'image_credit': product_data.get('image_credit', ''),
                    'image_source_url': product_data.get('image_source_url', ''),
                }
                if not product_data.get('image_url'):
                    defaults['image'] = product_data.get('image', '')

                product, _ = Product.objects.update_or_create(
                    slug=product_data['slug'],
                    defaults=defaults,
                )
                self.download_image(
                    product,
                    'image',
                    product_data.get('image_url'),
                    product_data.get('image_filename'),
                )

        self.stdout.write(self.style.SUCCESS(f'Seeded {Product.objects.count()} products.'))

    def seed_blog(self):
        data = self.load_json('blog/fixtures/blog_data.json')
        post_count = 0

        Post.objects.filter(
            author__email='dr.meow@petshop.com',
            slug__in=self.legacy_post_slugs,
        ).delete()

        for author_data in data:
            author, _ = Author.objects.update_or_create(
                email=author_data['email'],
                defaults={
                    'name': author_data['name'],
                    'bio': author_data.get('bio', ''),
                    'profile_picture': author_data.get('profile_picture', ''),
                },
            )

            for post_data in author_data.get('posts', []):
                post, _ = Post.objects.update_or_create(
                    slug=post_data['slug'],
                    defaults={
                        'author': author,
                        'title': post_data['title'],
                        'description': post_data['description'],
                        'body': post_data['body'],
                        'featured_image_alt': post_data.get('featured_image_alt', ''),
                        'image_credit': post_data.get('image_credit', ''),
                        'image_source_url': post_data.get('image_source_url', ''),
                    },
                )
                self.download_image(
                    post,
                    'featured_image',
                    post_data.get('image_url'),
                    post_data.get('image_filename'),
                )
                post.related_categories.set(
                    Category.objects.filter(slug__in=post_data.get('related_categories', []))
                )
                post.related_products.set(
                    Product.objects.filter(slug__in=post_data.get('related_products', []))
                )
                post_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {post_count} blog posts.'))

    def download_image(self, instance, field_name, url, filename):
        if self.skip_images or not url or not filename:
            return

        field_file = getattr(instance, field_name)
        image_exists = field_file.name and field_file.storage.exists(field_file.name)
        if image_exists and not self.refresh_images:
            return

        image_data = self.image_cache.get(url)
        if image_data is None:
            request = Request(url, headers={'User-Agent': 'Meowsalid seed_data/1.0'})
            for attempt in range(3):
                try:
                    with urlopen(request, timeout=30) as response:
                        content_type = response.headers.get_content_type()
                        if not content_type.startswith('image/'):
                            raise ValueError(f'unexpected content type {content_type}')
                        image_data = response.read(8 * 1024 * 1024 + 1)
                        if len(image_data) > 8 * 1024 * 1024:
                            raise ValueError('image is larger than 8 MB')
                    self.image_cache[url] = image_data
                    break
                except HTTPError as exc:
                    if exc.code != 429 or attempt == 2:
                        self.stderr.write(self.style.WARNING(f'Could not download {url}: {exc}'))
                        return
                    time.sleep(2 ** attempt)
                except (URLError, TimeoutError, ValueError) as exc:
                    self.stderr.write(self.style.WARNING(f'Could not download {url}: {exc}'))
                    return

        if field_file.name:
            field_file.delete(save=False)
        field_file.save(filename, ContentFile(image_data), save=True)
        self.stdout.write(f'Downloaded {filename}')
