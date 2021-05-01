from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_delete

def upload_location(instance, filename, **kwargs):
    file_path = "profile_pic/{user_id}/{user_username}-{filename}".format(
        user_id=str(instance.author.id), user_username=str(instance.title), filename=filename
    )
    return file_path

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True, blank=True, upload_to=upload_location)
    post_limit = models.PositiveIntegerField(default=2)
    update_limit = models.PositiveIntegerField(default=2)
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    group_name = models.CharField(max_length=60, null=False, blank=False, default='staff')

    def __str__(self):
        return self.user.username

@receiver(post_delete, sender=Profile)
def submission_delete(sender, instance, **kwargs):
    instance.profile_pic.delete(False)


class PostNum(models.Model):
    event_limit = models.PositiveIntegerField(default=10)
    blog_limit = models.PositiveIntegerField(default=10)

    def __str__(self):
        return "Limits"