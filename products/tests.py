from django.core.management import call_command
from django.test import TestCase

from blog.models import Post

from .models import Product


class SeedDataTests(TestCase):
    def test_seed_data_is_repeatable(self):
        call_command('seed_data', skip_images=True, verbosity=0)
        call_command('seed_data', skip_images=True, verbosity=0)

        self.assertEqual(Product.objects.count(), 17)
        self.assertEqual(Post.objects.count(), 5)
        post = Post.objects.get(slug='indoor-cat-enrichment-ideas')
        self.assertTrue(post.body.startswith('<p>'))
        self.assertEqual(
            list(post.related_products.values_list('slug', flat=True)),
            ['catnip-mouse', 'feather-wand', 'interactive-treat-puzzle'],
        )
