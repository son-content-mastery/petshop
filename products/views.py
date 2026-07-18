from django.shortcuts import render, get_object_or_404

from blog.models import Post

from .models import Category, Product


def product_detail(request, product_slug):
    # Get the product and its category
    product = get_object_or_404(Product, slug=product_slug, available=True)
    category = product.category

    # Query related products (same category, exclude current product)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    related_posts = Post.objects.filter(
        related_products=product,
    ).select_related('author').order_by('-date_created')[:3]

    context = {
        'category': category,
        'product': product,
        'related_products': related_products,
        'related_posts': related_posts,
    }
    return render(request, 'products/product-detail.html', context)


def category_detail(request, category_slug):
    # Get the category
    category = get_object_or_404(Category, slug=category_slug)

    # Get products and FAQs for the category
    products = category.products.filter(available=True)
    faqs = category.faqs.all()
    related_posts = Post.objects.filter(
        related_categories=category,
    ).select_related('author').order_by('-date_created')[:4]

    context = {
        'category': category,
        'products': products,
        'faqs': faqs,
        'related_posts': related_posts,
    }
    return render(request, 'products/category.html', context)
