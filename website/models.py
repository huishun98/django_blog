from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify

import requests
import string
import random

from froala_editor.fields import FroalaField

from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True, null=False)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category, related_name='articles')
    content = FroalaField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    saved_at = models.DateTimeField(auto_now=True)

    def snippet(self):
        return self.description[:50] + '...'
    
    def __str__(self):
        return self.slug


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists or (slug == 'new-post') or not slug:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Article)
