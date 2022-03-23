from django.shortcuts import render, redirect
from .models import Category, Photo
from django.contrib import messages


def gallery(request):
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)


def view_photo(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


def add_photo(request):
    categories = Category.objects.all()
    context = {'categories': categories}

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != "":
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            messages.error(request, 'You must choose or create a category.')
            return render(request, 'photos/new_photo.html', context)

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/new_photo.html', context)

