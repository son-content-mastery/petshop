from django.shortcuts import render, get_object_or_404, redirect
from .models import Post 
from products.models import Product, Category


def home(request):
    all_posts = Post.objects.select_related('author').order_by('-date_created')[:3]
    featured_product_slugs = [
        'indoor-balance-chicken-1-5kg',
        'ocean-recipe-tuna-in-broth-70g',
        'freeze-dried-chicken-bites-40g',
        'interactive-treat-puzzle',
    ]
    products_by_slug = {
        product.slug: product
        for product in Product.objects.filter(
            available=True,
            slug__in=featured_product_slugs,
        ).select_related('category')
    }
    products = [
        products_by_slug[slug]
        for slug in featured_product_slugs
        if slug in products_by_slug
    ]
    categories = Category.objects.order_by('name')
    hero_post = Post.objects.filter(
        slug='choose-dry-cat-food-by-age-and-lifestyle',
    ).first()

    context = {
        'all_posts': all_posts,
        'products': products,
        'categories': categories,
        'hero_post': hero_post,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    posts = Post.objects.select_related('author').order_by('-date_created')
    return render(request, 'blog/blog-list.html', {'posts': posts})


def post_detail(request, slug):
    single_post = get_object_or_404(
        Post.objects.select_related('author').prefetch_related(
            'related_categories',
            'related_products',
        ),
        slug=slug,
    )

    # Query recent articles (exclude the current post and limit to 3)
    recent_articles = (
        Post.objects.exclude(id=single_post.id)  # Exclude the current post
        .order_by('-date_updated')[:3]  # Get the 3 most recent articles
    )

    context = {
        'single_post': single_post,
        'recent_articles': recent_articles,
        'related_categories': single_post.related_categories.all(),
        'related_products': single_post.related_products.filter(available=True),
    }
    return render(request, 'blog/blog-detail.html', context)


def contact(request):
    if request.method == 'POST':
        return redirect('contact_success')

    return render(request, 'blog/contact.html')


def contact_success(request):
    return render(request, 'blog/contact-success.html')
