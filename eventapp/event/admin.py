from django.contrib import admin
from .models import *

class EventAdminView(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'reg_to', 'fee', 'date_updated', 'author']


admin.site.register(EventPost, EventAdminView)
admin.site.register(EventCategory)