from django.contrib import admin
from .models import Category, Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('category', 'description', 'user')
    list_display_links = ('description',)


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category)

