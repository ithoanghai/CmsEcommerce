from django import template
from django.conf import settings
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def stripe_public_key():
    if settings.STRIPE_PUBLIC_KEY:
        return mark_safe("'%s'" % conditional_escape(settings.STRIPE_PUBLIC_KEY))
    else:
        return "*** STRIPE_PUBLIC_KEY NOT SET ***"
