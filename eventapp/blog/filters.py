import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter
from .models import *
from django import forms

class BlogFilter(django_filters.FilterSet):
    CATERGORY_CHOICES = []

    for category in Category.objects.all():
        CATERGORY_CHOICES.append((str(category.name), str(category.name)))

    title = CharFilter(field_name="title", lookup_expr='icontains')
    author = CharFilter(field_name="author", lookup_expr='icontains')
    date_updated = DateFilter(field_name="date_updated", lookup_expr='exact')
    category = ChoiceFilter(choices=CATERGORY_CHOICES)

       
    class Meta:
        model = BlogPost
        fields = '__all__'
        exclude = ['body', 'image', 'date_published','slug']