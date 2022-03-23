from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Photo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    image = models.ImageField()
    description = models.TextField()

    def __str__(self):
        return self.description

