from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogslist, name="blogslist"),
    path("create/", views.create_blog, name="create-blog"),
    path("<slug>/", views.blog_detail, name="blog-detail"),
    path("<slug>/edit/", views.edit_blog, name="edit-blog"),
    path("<slug>/delete/", views.delete_blog, name="delete-blog"),
]
