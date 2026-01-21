from operator import truediv
from time import strptime
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse

from django.db import models
import datetime
from datetime import date, timedelta

from django.conf import settings
from django.db.models import OrderBy, TextField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from embed_video.fields import EmbedVideoField

from symtable import Class
from django.db import models


import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.views.generic import ListView, DetailView, CreateView, UpdateView

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    summary = CKEditor5Field(config_name='extends', blank=True, null=True)
    content = CKEditor5Field(config_name='extends', blank=True, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_image = models.ImageField(upload_to='uploads/article/', blank=True, null=True)
    article_file = models.FileField(upload_to='uploads/files/', blank=True, null=True)

    def __str__(self):
        return self.title + "-" + self.author.username

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = CKEditor5Field(config_name='extends', blank=True, null=True)
    text = TextField()

class ArticleCreateView(CreateView):
    model = Article
    template_name = 'post_article.html'
    fields = '__all__'

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'article_update.html'
    fields = '__all__'
