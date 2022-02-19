from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


# @login_required
# def helth(req):
#     return render(req, "helth.html")

app_name = "Nady_System"


@login_required
def home(req):
    return render(req, f"{app_name}/home.html")


def about(req):
    return render(req, f"{app_name}/about.html")


def services(req):
    return render(req, f"{app_name}/services.html")


def appointment(req):
    return render(req, f"{app_name}/appointment.html")


def gallery(req):
    return render(req, f"{app_name}/gallery.html")


def team(req):
    return render(req, f"{app_name}/team.html")


def blog(req):
    return render(req, f"{app_name}/blog.html")


def contact(req):
    return render(req, f"{app_name}/contact.html")
