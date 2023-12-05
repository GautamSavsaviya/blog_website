from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
import datetime


# Create custom model manager that return only not soft deleted data
class CustomManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_deleted=False)


# Create base model for all models that contains soft delete functionality
class SoftDelete(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = CustomManager()  # overwrite with custom model manager
    every = models.Manager()  # create new model manage that works as built in model manager

    def delete_obj(self):
        self.is_deleted = True
        self.save()

    def restore_obj(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True  # It indicates that this class is not model but it is a base class for models


# Create your models here.
class Blog(SoftDelete):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=300)
    description = models.TextField()
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to="blogs/images", default="default-blog.jpg")
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
