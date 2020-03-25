from django import template
from django.core.exceptions import ObjectDoesNotExist

from webapp.models import Rating

register = template.Library()


@register.filter
def can_review(user, movie):
    try:
        Rating.objects.get(reviewer=user, movie=movie)
        return False
    except ObjectDoesNotExist:
        return True
