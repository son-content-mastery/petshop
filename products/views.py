from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_detail(request, product_slug):
    # Get the product and its category
    product = get_object_or_404(Product, slug=product_slug, available=True)
    category = product.category

    # Query related products (same category, exclude current product)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    context = {
        'category': category,
        'product': product,
        'related_products': related_products
    }
    return render(request, 'products/product-detail.html', context)


def category_detail(request, category_slug):
    # Get the category
    category = get_object_or_404(Category, slug=category_slug)

    # Get products and FAQs for the category
    products = category.products.filter(available=True)
    faqs = category.faqs.all()

    context = {
        'category': category,
        'products': products,
        'faqs': faqs,
    }
    return render(request, 'products/category.html', context)