from django.urls import path
from . import views

urlpatterns = [
    path('', views.eventlist, name="eventslist"),
    path("create/", views.create_event, name="create-event"),
    path("<slug>/", views.event_detail, name="event-detail"),
    path("<slug>/edit/", views.edit_event, name="edit-event"),
    path("<slug>/delete/", views.delete_event, name="delete-event"),
]
