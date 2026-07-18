from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product

from .models import Post


class ContactPageTests(TestCase):
    def test_contact_page_renders(self):
        response = self.client.get(reverse('contact'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')

    def test_contact_submission_redirects_to_success_page(self):
        response = self.client.post(
            reverse('contact'),
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'phone': '0123456789',
                'message': 'Testing the contact flow.',
            },
        )

        self.assertRedirects(response, reverse('contact_success'))

    def test_contact_success_page_renders(self):
        response = self.client.get(reverse('contact_success'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/contact/success/')


class BlogPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='อาหารเม็ด', slug='dry-food')
        cls.product = Product.objects.create(
            category=cls.category,
            name='Indoor Cat Food',
            slug='indoor-cat-food',
            description='Food for indoor cats',
            body='<p>Product HTML</p>',
            price='399.00',
        )
        cls.post = Post.objects.create(
            title='คู่มือเลือกอาหารแมว',
            slug='cat-food-guide',
            description='เลือกอาหารให้เหมาะกับแมว',
            body='<h2>เนื้อหา HTML</h2><p><a href="/dry-food/">ดูอาหารเม็ด</a></p>',
        )
        cls.post.related_categories.add(cls.category)
        cls.post.related_products.add(cls.product)

    def test_blog_index_renders_at_blog_path(self):
        response = self.client.get(reverse('post_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.get_absolute_url())

    def test_blog_detail_renders_summernote_html_and_related_links(self):
        response = self.client.get(self.post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>เนื้อหา HTML</h2>', html=True)
        self.assertNotContains(response, '&lt;h2&gt;')
        self.assertContains(response, self.category.get_absolute_url())
        self.assertContains(response, self.product.get_absolute_url())

    def test_category_and_product_link_back_to_related_post(self):
        category_response = self.client.get(self.category.get_absolute_url())
        product_response = self.client.get(self.product.get_absolute_url())

        self.assertContains(category_response, self.post.get_absolute_url())
        self.assertContains(product_response, self.post.get_absolute_url())


class SeoEndpointTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='อาหารเม็ด', slug='dry-food')
        cls.available_product = Product.objects.create(
            category=cls.category,
            name='Available Food',
            slug='available-food',
            description='Available product',
            price='200.00',
        )
        cls.unavailable_product = Product.objects.create(
            category=cls.category,
            name='Unavailable Food',
            slug='unavailable-food',
            description='Unavailable product',
            price='200.00',
            available=False,
        )
        cls.hero_post = Post.objects.create(
            title='เลือกอาหารเม็ดให้แมว',
            slug='choose-dry-cat-food-by-age-and-lifestyle',
            description='Hero article',
            body='<p>Article</p>',
            featured_image='blog_images/hero.jpg',
            featured_image_alt='แมวกำลังกินอาหารเม็ด',
        )

    def test_robots_txt_allows_public_pages_and_points_to_sitemap(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'Allow: /')
        self.assertContains(response, 'Disallow: /admin/')
        self.assertContains(response, 'Disallow: /contact/success/')
        self.assertContains(response, 'Sitemap: https://meowsalid.com/sitemap.xml')

    def test_sitemap_contains_public_content_only(self):
        response = self.client.get(reverse('sitemap'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        self.assertContains(response, self.category.get_absolute_url())
        self.assertContains(response, self.available_product.get_absolute_url())
        self.assertContains(response, self.hero_post.get_absolute_url())
        self.assertNotContains(response, self.unavailable_product.get_absolute_url())
        self.assertNotContains(response, reverse('contact_success'))

    def test_home_uses_seeded_hero_and_new_footer_links(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/media/blog_images/hero.jpg')
        self.assertContains(response, 'Meowsalid.')
        self.assertContains(response, self.category.get_absolute_url())
        self.assertContains(response, reverse('sitemap'))
