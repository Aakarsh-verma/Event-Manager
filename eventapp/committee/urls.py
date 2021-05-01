from django.urls import path
from . import views

app_name = "committee"

urlpatterns = [
    path('', views.committeelist, name="committee"),
    path("<slug>/", views.detail_committee_view, name="committee-detail"),
    path("<slug>/edit/", views.edit_committee_view, name="edit-committee"),
]
