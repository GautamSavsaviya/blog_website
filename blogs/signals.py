from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Blog
from django.utils.text import slugify
import uuid

@receiver(pre_save, sender=Blog)
def generate_blog_slug(sender, instance, *args, **kwargs):
    if instance.slug is None:
        instance.slug = f'{slugify(instance.title)}-{str(uuid.uuid4())[:8]}'
    elif instance.slug[:-9] != slugify(instance.title):
        instance.slug = f'{slugify(instance.title)}-{str(uuid.uuid4())[:8]}'
