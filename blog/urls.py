from django.urls import path

from .views import contact, contact_success, home, post_detail, post_list


urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('contact/success/', contact_success, name="contact_success"),
    path('blog/', post_list, name="post_list"),
    path('blog/<slug:slug>/', post_detail, name="post_detail"),
]
