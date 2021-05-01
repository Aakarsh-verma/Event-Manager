from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

from .models import  Committee
from .filters import CommitteeFilter
from .forms import  UpdateCommitteeForm
from event.models import EventPost, EventCategory
from event.filters import EventFilter

POST_PER_PAGE = 5
# List of All blogs

def committeelist(request):
    context = {}
    
    committee = Committee.objects.all().order_by('date_updated').reverse()

    myFilter = CommitteeFilter(request.GET, queryset=committee)
    committee = myFilter.qs

    context['committee'] = committee

    return render(request, 'committee/committee_home.html', context)

def detail_committee_view(request, slug):
    context = {}

    committee = get_object_or_404(Committee, slug=slug)
    context["committee"] = committee

    categories = EventCategory.objects.all()
    event_posts = EventPost.objects.filter(author=committee.author)
    myFilter = EventFilter(request.GET, queryset=event_posts)
    events = myFilter.qs

    # Pagination
    page = request.GET.get("page", 1)
    event_posts_paginator = Paginator(event_posts, POST_PER_PAGE)

    try:
        event_posts = event_posts_paginator.page(page)
    except PageNotAnInteger:
        event_posts = event_posts_paginator.page(POST_PER_PAGE)
    except EmptyPage:
        event_posts = event_posts_paginator.page(event_posts_paginator.num_pages)

    context['event_posts'] = event_posts
    context['categories'] = categories

    return render(request, "committee/detail_committee.html", context)

def edit_committee_view(request, slug):
    context = {}

    user = request.user
    if not user.is_authenticated:
        return redirect("must_authenticate")

    committee = get_object_or_404(Committee, slug=slug)

    if committee.author != user:
        return HttpResponse("You are not the author of that post.")

    if request.POST:
        form = UpdateCommitteeForm(
            request.POST or None, request.FILES or None, instance=committee
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.success(request, f"Update successfull!")
            committee = obj
            return redirect("../../{}/".format(committee.slug))

    form = UpdateCommitteeForm(
        initial={
            "name": committee.name,
            "description": committee.description,
            "link": committee.link,
            "image": committee.image,
            # "back_image": committee.back_image,
        }
    )

    context["form"] = form
    return render(request, "committee/edit_committee.html", context)