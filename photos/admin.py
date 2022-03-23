from django.contrib import admin
from .models import Category, Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('category', 'description')
    list_display_links = ('description',)


"""class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name'
    list_display_links = 'name'"""


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category)

