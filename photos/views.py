from django.shortcuts import render, redirect, Http404, get_object_or_404
from .models import Category, Photo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='accounts/login')
def gallery(request):
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.filter(user=request.user)
    else:
        photos = Photo.objects.filter(
            Q(category__name=category) &
            Q(user=request.user)
        )
            
    categories = Category.objects.all()
    context = {'categories': categories, 'photos': photos}
    return render(request, 'photos/gallery.html', context)

def view_photo(request, pk):    
    photo = get_object_or_404(Photo, id=pk)
    
    if request.user != photo.user: 
        raise Http404()

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
            user=request.user,
        )

        messages.success(request, 'New Photo created.')
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/new_photo.html', context)

