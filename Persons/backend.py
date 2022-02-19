from typing import Any, Optional
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from django.contrib.auth.models import AbstractBaseUser


class MyBackEnd(ModelBackend):
    def authenticate(
        self, request: Optional[HttpRequest], **kwargs: Any
    ) -> Optional[AbstractBaseUser]:
        return super().authenticate(request, **kwargs)

    def get_user(self, user_id: int) -> Optional[AbstractBaseUser]:
        return super().get_user(user_id)
