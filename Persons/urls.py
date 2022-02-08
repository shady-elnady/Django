from django.urls import path
from .views import signUp


app_name = "Persons"


urlpatterns = [
    path("signUp/", signUp, name="signUp"),
]
