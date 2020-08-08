from django.db import models
from django.utils import timezone

# Create your models here.
"""
Author
- name, str, max length - 80 chars

Article
- title, str, max length - 50 chars
- body, textfield
- post date - datetime
- author - foreignkey (one to many relationship)
"""


class Author(models.Model):
    name = models.CharField(max_length=80)
    bio = models.TextField(default="Pending")

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField()
    instructions = models.TextField(default="Pending")
    time_required = models.CharField(max_length=50, default="Pending")
    post_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.author.name}"
