from django.http import HttpResponse
from django.shortcuts import redirect
from .models import EventPost

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('../create/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def unauthenticated_author(view_func):
    def wrapper_func(request, slug, *args, **kwargs):
        user = request.user
        if user.is_authenticated and EventPost.objects.filter(slug=slug, author=user).exists():
            return
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func