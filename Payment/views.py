from django.shortcuts import render

# Create your views here.

app_name = "Payment"


def paypal(req):
    context = {"app_name": app_name}
    return render(req, f"{app_name}/paypal.html", context=context)
