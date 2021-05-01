from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User



def upload_location(instance, filename, **kwargs):
    file_path = "blog/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    CATERGORY_CHOICES = []

    for category in Category.objects.all():
        CATERGORY_CHOICES.append((str(category.name), str(category.name)))

    title = models.CharField(max_length=120, unique=True,null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to=upload_location)
    date_published = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True)
    category = models.CharField(max_length=100, choices=CATERGORY_CHOICES, default="null")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
