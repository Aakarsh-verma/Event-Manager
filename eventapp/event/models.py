from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver

def upload_location(instance, filename, **kwargs):
    file_path = "event/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path

class EventCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EventPost(models.Model):

    CATERGORY_CHOICES = []
    for event_category in EventCategory.objects.all():
        CATERGORY_CHOICES.append((str(event_category.name), str(event_category.name)))
    
    title = models.CharField(max_length=100, null=False, blank=False)
    body = models.TextField(max_length=1200, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    category = models.CharField(max_length=100, choices=CATERGORY_CHOICES, default="null")
    event_date = models.DateField(auto_now_add=False, null=False, blank=False)
    reg_to = models.DateField(auto_now_add=False, null=False, blank=False)
    fee = models.PositiveIntegerField(default=0)
    reg_link = models.URLField(null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)
    priority = models.IntegerField(default=0)
    day_rem = models.IntegerField(default=0)


    def __str__(self):
        return self.title

@receiver(post_delete, sender=EventPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_event_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_event_post_receiver, sender=EventPost)
