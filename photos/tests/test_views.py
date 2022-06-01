from django.test import TestCase, Client
from django.contrib.auth.models import User
from photos.models import Photo, Category
from django.urls import reverse
import tempfile


class GalleryViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('gallery')
        self.username = 'name_test'        
        self.password = 'pass_test'
        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save() 

        self.category = Category.objects.create(
            name='test_category',
        )
        self.photo = Photo.objects.create(
            user=self.user,
            category=self.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            description='testing'
        )

    def test_gallery_view_deny_anonymous(self):
        response = self.client.get(self.url)  
        self.assertEquals(response.status_code, 302)      
        self.assertRedirects(response, '/accounts/login?next=/',
        fetch_redirect_response=False)
        
        response = self.client.post(self.url)  
        self.assertEquals(response.status_code, 302)      
        self.assertRedirects(response, '/accounts/login?next=/',
        fetch_redirect_response=False)

    def test_gallery_view_load_login_users(self):
        self.client.login(username=self.username, 
                          password=self.password)
        response = self.client.get(self.url)    

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos/gallery.html')
        self.assertIn('categories', response.context) 
        self.assertIn('photos', response.context) 


class ViewPhotoTest(TestCase):
    
    def setUp(self):
        self.client = Client()        
        
        self.username = 'name_test'        
        self.password = 'pass_test'
        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save() 

        self.category = Category.objects.create(name='test_category',)
        self.photo = Photo.objects.create(
            user=self.user,
            category=self.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            description='testing'
        )
        self.photo_instance = Photo.objects.get(id=1)
        self.url = f"'photo'/{self.photo_instance.id}"

    def test_view_photo(self):                
        self.client.login(username=self.username, 
                          password=self.password)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos/photo.html')
        self.assertTrue('photo' in response.context) 
    
    def test_view_photo_deny_anonymous(self):
        response = self.client.get(self.url)  
        self.assertEquals(response.status_code, 3202)      
        self.assertRedirects(response, '/aaccounts/login?next=/',
        fetch_redirect_response=False)
        
        response = self.client.post(self.url)  
        self.assertEquals(response.status_code, 3202)      
        self.assertRedirects(response, '/aaccounts/login?next=/',
        fetch_redirect_response=False)

    def test_view_photo_load_login_users(self):
        self.client.login(username=self.username, 
                          password=self.password)
        response = self.client.get(self.url)    

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos/gallery.html')
        self.assertIn('categories', response.context) 
        self.assertIn('photos', response.context) 


class AddPhotoTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('gallery')
        self.username = 'name_test'        
        self.password = 'pass_test'
        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save() 

        self.category = Category.objects.create(
            name='test_category',
        )
        self.photo = Photo.objects.create(
            user=self.user,
            category=self.category,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            description='testing'
        )
        self.photo_instance = Photo.objects.get(id=1)

    def test_view_ok(self):                
        self.client.login(username=self.username, 
                          password=self.password)
        self.url = reverse('add_photo')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'photos/new_photo.html')
        self.assertTrue('categories' in response.context) 

    def test_view_post(self):
        self.client.login(username=self.username, 
                          password=self.password) 
        data = {
            'category': self.photo.category.id,
            'description': self.photo.description,
            'image': tempfile.NamedTemporaryFile(suffix=".png").name,
            'user': self.photo.user.id,
        }        
        response = self.client.post('/add/', data=data)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Photo.objects.count(), 2)
        

