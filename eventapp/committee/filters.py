import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter, ChoiceFilter
from .models import Committee
from django import forms

class CommitteeFilter(django_filters.FilterSet):
    name = CharFilter(field_name="name", lookup_expr='icontains')

       
    class Meta:
        model = Committee
        fields = ['name']

