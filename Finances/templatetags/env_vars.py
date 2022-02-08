from django import template
from django.template.defaultfilters import stringfilter
from decouple import config

# from django.template.defaulttags import register
# import os


register = template.Library()


@register.filter(name="env")
@stringfilter
def env(key):
    # return os.environ.get(key, None)
    return config(key)
