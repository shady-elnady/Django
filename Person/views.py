from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.conf import settings

from .forms import SignUpForm

# Create your views here.


def signUp(req):
    if req.method == "POST":
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(req, user)
            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = SignUpForm()

    context = {
        "form": form,
    }

    return render(req, "registration/signUp.html", context=context)
