"""Config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from GraphQL.views import GraphQLPlaygroundView
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

# from Nady_System.views import helth


urlpatterns = [
    path("entity/", include("django_spaghetti.urls")),
    path(
        "graphql",
        csrf_exempt(
            FileUploadGraphQLView.as_view(
                graphiql=False,
            )
        ),
    ),
    path(
        "playground",
        csrf_exempt(GraphQLPlaygroundView.as_view(endpoint="/graphql")),
    ),
    path("__debug__/", include(debug_toolbar.urls)),
    path("i18n/", include("django.conf.urls.i18n")),
]


urlpatterns += i18n_patterns(
    path("", include("Nady_System.urls")),
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    # path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/", include("Persons.urls", namespace="accounts")),
    path("payment/", include("Payment.urls", namespace="payment")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
