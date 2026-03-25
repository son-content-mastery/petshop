from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('blog.urls')),
    
    # Products inclusion at root and bottom as catch-all for categories
    path('', include('products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)