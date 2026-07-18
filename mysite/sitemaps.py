from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Post
from products.models import Category, Product


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return ['home', 'post_list', 'contact']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == 'home' else 0.7


class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Category.objects.order_by('slug')


class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Product.objects.filter(available=True).order_by('slug')

    def lastmod(self, item):
        return item.updated


class PostSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8

    def items(self):
        return Post.objects.exclude(slug__isnull=True).exclude(slug='').order_by('slug')

    def lastmod(self, item):
        return item.date_updated


sitemaps = {
    'static': StaticViewSitemap,
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'posts': PostSitemap,
}
