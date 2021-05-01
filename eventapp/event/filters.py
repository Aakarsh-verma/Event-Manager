import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter
from .models import *
from django import forms

class EventFilter(django_filters.FilterSet):
    CATERGORY_CHOICES = []
    for category in EventCategory.objects.all():
        CATERGORY_CHOICES.append((str(category.name), str(category.name)))
    
    FEE_CHOICES = []
    for fees in EventPost.objects.all():
        FEE_CHOICES.append((str(fees.fee), str(fees.fee)))

    title = CharFilter(field_name="title", lookup_expr='icontains')
    author = CharFilter(field_name="author", lookup_expr='icontains')
    event_date = DateFilter(field_name="event_date", lookup_expr='exact')
    reg_to = DateFilter(field_name="reg_to", lookup_expr='exact')
    date_updated = DateFilter(field_name="date_updated", lookup_expr='exact')
    category = ChoiceFilter(choices=CATERGORY_CHOICES)
    fee = ChoiceFilter(field_name="fee", choices=FEE_CHOICES, lookup_expr='exact')
       
    class Meta:
        model = EventPost
        fields = ['title', 'author','event_date', 'reg_to', 'date_updated', 'category', 'fee']