from django.contrib import admin
from .models import BlogPost, Category

class BlogAdminView(admin.ModelAdmin):
    list_display = ['title', 'date_updated', 'author']


admin.site.register(BlogPost, BlogAdminView)
admin.site.register(Category)