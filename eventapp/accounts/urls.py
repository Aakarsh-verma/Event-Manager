from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #profile urls
    path("youraccount/", views.account_view, name="account"),
    path("profile/redirect", views.create_default_profile, name="default-profile"),
    path("profile/<int:id>/", views.create_profile_view, name="create-profile"),
    path("author/<int:id>/", views.author_view, name="author-view"),

    #limiturls
    path("limit_reached", views.limit_reached_view, name="limit_reached"),
    path("must_authenticate", views.must_authenticate_view, name="must_authenticate"),

    #auth urls
    # path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Password Reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),
    
]