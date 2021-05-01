from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .models import EventPost, EventCategory
from .forms import CreateEventPostForm, UpdateEventPostForm
from .filters import EventFilter
from accounts.models import Profile, PostNum

from datetime import datetime, timedelta


# List of All blogs
limit = PostNum.objects.all().first()
POST_PER_PAGE = limit.blog_limit
# List of All blogs
def eventlist(request):
    context = {}
    
    events = EventPost.objects.all().order_by('date_updated').reverse()
    categories = EventCategory.objects.all()
    now = datetime.today().date()

    fees = []
    for i in EventPost.objects.all():
        if i.fee not in fees:
            fees.append(int(i.fee))

    for event in events:
        day_rem = event.reg_to - now
        EventPost.objects.filter(id=event.id).update(day_rem=day_rem.days)

    myFilter = EventFilter(request.GET, queryset=events)
    events = myFilter.qs

    # Pagination
    page = request.GET.get("page", 1)
    event_posts_paginator = Paginator(events, POST_PER_PAGE)

    try:
        events = event_posts_paginator.page(page)
    except PageNotAnInteger:
        events = event_posts_paginator.page(POST_PER_PAGE)
    except EmptyPage:
        events = event_posts_paginator.page(event_posts_paginator.num_pages)

    context['events'] = events
    context['fees'] = fees
    context['categorys'] = categories

    return render(request, 'event/event_home.html', context)

# Detail of a particular event
def event_detail(request, slug):
    context = {}

    event_post = get_object_or_404(EventPost, slug=slug)
    context['event_post'] = event_post

    return render(request, 'event/event_detail.html', context)

# Create a new event

def create_event(request):
    context = {}

    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate")
    
    event_posts = EventPost.objects.filter(author=user)
    context["event_posts"] = event_posts
    limit = 0
    for post in event_posts:
        event_date = post.date_published.date()
        today = datetime.now().date()
        if today == event_date:
            limit += 1

    if not user.is_superuser:
        if limit >= user.profile.post_limit:
            return redirect("limit_reached")
    
    form = CreateEventPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = request.user
        obj.author = author
        obj.save()
        messages.success(
            request, f"Your Event has been posted successfully!"
        )
        return redirect("eventslist")

    else:
        form = CreateEventPostForm()
        context["form"] = form
        return render(request, "event/create_event.html", context)


def edit_event(request, slug):

    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect("must_authenticate")

    event_post = get_object_or_404(EventPost, slug=slug)

    # categorys = Category.objects.all()
    # context["categorys"] = categorys
    
    # event_posts = EventPost.objects.filter(author=user)
    # context["event_posts"] = event_posts

    # limit = []
    # edate = blog_post.date_updated.strftime("%Y-%m-%d")
    # edate0 = datetime.strptime(edate, "%Y-%m-%d").date()
    # if today == edate0:
    #     limit.append(edate0)

    # if user.is_staff == 1:
    #     if len(limit) >= user.post_limit:
    #         return redirect("limit_reached")

    if event_post.author != user:
        return HttpResponse("You are not the author of that post.")

    form = UpdateEventPostForm(
        request.POST or None, request.FILES or None, instance=event_post
    )
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, f"Your Post has been updated successfully!")
        blog_post = obj
        return redirect("eventslist")

    form = UpdateEventPostForm(
        initial={
            "title": event_post.title,
            "body": event_post.body,
            "image": event_post.image,
            "category": event_post.category,
            "event_date": event_post.event_date,
            "reg_to": event_post.reg_to,
            "fee": event_post.fee,
            "reg_link": event_post.reg_link,
        }
    )

    context["form"] = form

    return render(request, "event/edit_event.html", context)

def delete_event(request, slug):
    context = {}
    user = request.user

    event_post = get_object_or_404(EventPost, slug=slug)

    if event_post.author != user:
        return HttpResponse("You are not the author of that post.")
    
    if request.method == "POST":
        event_post.delete()
        messages.success(request, f"Your Post has been deleted successfully!")
        return redirect("eventslist")

    context["event_post"] = event_post
    return render(request, "event/delete_event.html", context)
