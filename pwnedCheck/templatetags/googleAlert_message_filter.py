# __author__ = "Aditi Sharma"

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def strSplit(value):
    value = value.split("⋅")
    return value[1]