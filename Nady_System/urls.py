from django.urls import path
from .views import index, home, about, services, appointment, gallery, team, blog, contact

app_name = 'Nady_System'

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('appointment/', appointment, name='appointment'),
    path('gallery/', gallery, name='gallery'),
    path('team/', team, name='team'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
]