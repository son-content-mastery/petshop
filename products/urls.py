from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product detail: /products/<product_slug>/
    path('products/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
    # Category detail as catch-all: /<category_slug>/
    path('<slug:category_slug>/', views.category_detail, name='category'),
]