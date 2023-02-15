from django import template

from django.urls import reverse
from django.urls.exceptions import Resolver404 as resolve404

register = template.Library()

@register.filter(name='url_check')
def url_check(value, _id):
    try:
        reverse(value, args={_id})
        return True
    except resolve404:
        return False