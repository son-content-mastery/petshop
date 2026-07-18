from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Author, Post


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ['title', 'author', 'date_updated']
    search_fields = ['title', 'description', 'body']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['related_categories', 'related_products']
    summernote_fields = ('body',)


admin.site.register(Author)
