from django.contrib import admin
from .models import Profile, PostNum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib import messages


class PostNumAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        if self.model.objects.count() >= 1:
            self.message_user(request, 'Only one entry can exist at once - please remove other first', messages.ERROR)
            return HttpResponseRedirect(reverse(f'admin:{self.model._meta.app_label}_postnum_changelist'))
        return super().add_view(request, form_url, extra_context)

admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(PostNum, PostNumAdmin)

admin.site.site_header = "PCE EventAdda Administration"