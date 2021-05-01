from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from event.models import EventPost, EventCategory
# from account.models import Account


# 1MB - 1048576
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "1048576"

CATERGORY_CHOICES = []
for category in EventCategory.objects.all():
    CATERGORY_CHOICES.append((str(category.name), str(category.name)))

class CreateEventPostForm(forms.ModelForm):

    category = forms.ChoiceField(choices=CATERGORY_CHOICES)

    class Meta:
        model = EventPost
        fields = [
            "title",
            "category",
            "body",
            "reg_to",
            "event_date",
            "fee",
            "reg_link",
            "image",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title.."}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Content.."}
            ),
            "fee": forms.NumberInput(attrs={"class": "form-control"}),
            "reg_link": forms.URLInput(attrs={"class": "form-control"}),
        }

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Registration Dates")

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        # content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image


class UpdateEventPostForm(forms.ModelForm):

    category = forms.ChoiceField(choices=CATERGORY_CHOICES)

    class Meta:
        model = EventPost
        fields = [
            "title",
            "category",
            "body",
            "reg_to",
            "event_date",
            "fee",
            "reg_link",
            "image",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title.."}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Content.."}
            ),
            "fee": forms.NumberInput(attrs={"class": "form-control"}),
            "reg_link": forms.URLInput(attrs={"class": "form-control"}),
        }

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        # content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image