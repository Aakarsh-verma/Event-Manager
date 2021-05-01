from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Profile
from .forms import CreateUserForm, UserUpdateForm, CreateProfileForm, ProfileUpdateForm

from event.models import EventPost
import requests
import simplejson as json

def login_view(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('eventslist')
        else:
            messages.warning(request, "Kindly Check your login Credentitals")
        
        # captcha_token = request.POST["g-recaptcha-response"]
        # cap_url = "https://www.google.com/recaptcha/api/siteverify"
        # cap_secret = "6Lfm5MUZAAAAADGzhmFEYLc-5lSVP-ZEeoAg0k95"
        # cap_data = {"secret": cap_secret, "response": captcha_token}
        # r = requests.post(
        #     "https://www.google.com/recaptcha/api/siteverify", data=cap_data
        # )
        # response = json.loads(r.text)
        # verify = response["success"]
        # print(verify)

        # user = authenticate(username=username, password=password)
        # if verify == True:

        #     if user:
        #         login(request, user)
        #         return redirect("event-home")
        # else:
        #     messages.error(request, f"INVALID CAPTCHA..")
    
    return render(request, 'accounts/login.html', context)

def register_view(request):
    context = {}
    
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request, 'Account was created for '+ user)

        return redirect('login')
    context['form'] = form
    
    return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('eventslist')

@login_required
def account_view(request):

    context = {}
    user = request.user


    event_post = EventPost.objects.filter(author=user)
    if not Profile.objects.filter(user=request.user):
        return redirect("../profile/" + str(user.id))

    if request.POST:
        form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=user.profile,
        )
        if form.is_valid() and p_form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
                "first_name": request.POST["first_name"],
                "last_name": request.POST["last_name"],
            }

            p_form.initial = {
                "website_url": request.POST["website_url"],
                "facebook_url": request.POST["facebook_url"],
                "instagram_url": request.POST["instagram_url"],
                "youtube_url": request.POST["youtube_url"],
            }
            
            obj = p_form.save(commit=False)
            obj.save()
            form.save()
            messages.success(request, f"Profile Update successfull!")
    else:
        form = UserUpdateForm(
            initial={
                "email": user.email,
                "username": user.username,
            })
        p_form = ProfileUpdateForm(initial={
            "profile_pic": user.profile.profile_pic,
            "website_url": user.profile.website_url,
            "facebook_url": user.profile.facebook_url,
            "instagram_url": user.profile.instagram_url,
            "youtube_url": user.profile.youtube_url,
            })
    context["form"] = form
    context["p_form"] = p_form
    context["event_post"] = event_post

    return render(request, "accounts/account.html", context)

@login_required(login_url='login')
def create_profile_view(request, id):
    context = {}
    user = request.user
    if request.POST:
        form = CreateProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            messages.info(
                request, f"You can update your info anytime in your account page."
            )
            return redirect("profile")
    else:
        form = CreateProfileForm(initial = { 
                "user": request.user, 
                "profile_pic": "static/default_pic.png",
            })
    context["form"] = form
    return render(request, "accounts/create_profile.html", context)


@login_required(login_url='login')
def create_default_profile(request):
    user = request.user
    Profile.objects.create(user=user)
    return redirect('account')


def author_view(request, id):

    context = {}
    profile = Profile.objects.get(user_id=id)
    event_post = EventPost.objects.filter(author=profile.user)
    event_post = event_post.order_by("date_published").reverse()
    context["profile"] = profile
    context["event_post"] = event_post

    return render(request, "accounts/author.html", context)


def must_authenticate_view(request):
    return render(request, "accounts/must_authenticate.html", {})


def limit_reached_view(request):
    return render(request, "accounts/limit_reached.html", {})