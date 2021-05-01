from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .models import BlogPost, Category
from .forms import CreateBlogPostForm, UpdateBlogPostForm
from .filters import BlogFilter
from accounts.models import Profile, PostNum
from datetime import datetime

# List of All blogs
limit = PostNum.objects.all().first()
POST_PER_PAGE = limit.blog_limit
def blogslist(request):
    context = {}
    
    blogs = BlogPost.objects.all().order_by('date_updated').reverse()
    categories = Category.objects.all()
    myFilter = BlogFilter(request.GET, queryset=blogs)
    blogs = myFilter.qs

    # Pagination
    page = request.GET.get("page", 1)
    blog_posts_paginator = Paginator(blogs, POST_PER_PAGE)

    try:
        blogs = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blogs = blog_posts_paginator.page(POST_PER_PAGE)
    except EmptyPage:
        blogs = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blogs'] = blogs
    context['categories'] = categories

    return render(request, 'blog/blog_home.html', context)

# Detail of a particular blog
def blog_detail(request, slug):
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    context['blog_post'] = blog_post

    return render(request, 'blog/blog_detail.html', context)

def create_blog(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate")
    
    blog_posts = BlogPost.objects.filter(author=user)
    context["blog_posts"] = blog_posts

    limit = 0
    for post in blog_posts:
        event_date = post.date_published.date()
        today = datetime.now().date()
        if today != event_date:
            limit += 1

    if not user.is_superuser:
        if limit >= user.profile.post_limit:
            return redirect("limit_reached")
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = request.user
        obj.author = author
        obj.save()
        messages.success(
            request, f"Your Blog has been posted successfully!"
        )
        return redirect("blogslist")

    else:
        form = CreateBlogPostForm()
        context["form"] = form
        return render(request, "blog/create_blog.html", context)
    context = {}

    user = request.user
    
    if not user.is_authenticated:
        return redirect("must_authenticate")


def edit_blog(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate")

    blog_post = get_object_or_404(BlogPost, slug=slug)

    limit = 0
    if blog_post.exists():
        limit = user.profile.update_limit
        blog_date = blog_post.date_published.date()
        today = datetime.now().date()
        if today != blog_date:
            limit += 1
        
    if not user.is_superuser:
        if limit >= user.profile.post_limit:
            return redirect("limit_reached")

    if blog_post.author != user:
        return HttpResponse("You are not the author of that post.")

    form = UpdateBlogPostForm(
        request.POST or None, request.FILES or None, instance=blog_post
    )
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, f"Your Post has been updated successfully!")
        blog_post = obj
        return redirect("blogslist")

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "category": blog_post.category,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )

    context["form"] = form

    return render(request, "blog/edit_blog.html", context)

def delete_blog(request, slug):
    context = {}
    user = request.user

    blog_post = get_object_or_404(BlogPost, slug=slug)

    if blog_post.author != user:
        return HttpResponse("You are not the author of that post.")
    
    if request.method == "POST":
        blog_post.delete()
        messages.success(request, f"Your Post has been deleted successfully!")
        return redirect("blogslist")

    context["blog_post"] = blog_post
    return render(request, "blog/delete_blog.html", context)
