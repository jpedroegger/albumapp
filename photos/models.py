from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('view_photo', kwargs={'pk': self.id})

