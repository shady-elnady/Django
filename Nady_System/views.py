from django.shortcuts import render

# Create your views here.


def helth(req):
    return render(req, "helth.html")


def home(req):
    return render(req, "lab/home.html")


def about(req):
    return render(req, "lab/about.html")


def services(req):
    return render(req, "lab/services.html")


def appointment(req):
    return render(req, "lab/appointment.html")


def gallery(req):
    return render(req, "lab/gallery.html")


def team(req):
    return render(req, "lab/team.html")


def blog(req):
    return render(req, "lab/blog.html")


def contact(req):
    return render(req, "lab/contact.html")
