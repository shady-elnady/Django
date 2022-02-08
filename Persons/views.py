from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from django.conf import settings


# Create your views here.


def signUp(req):
    if req.method == "POST":
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            user = authenticate(username=username, email=email)
            login(req, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            print("form Not Valid")
    else:
        form = SignUpForm()

    return render(req, "registration/sginup.html", {"form": form})
