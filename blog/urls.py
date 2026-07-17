from django.urls import path 
from .views import home, post_detail, contact, contact_success


urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('contact/success/', contact_success, name="contact_success"),
    path('blog/<slug:slug>/', post_detail, name="post_detail") 
]

