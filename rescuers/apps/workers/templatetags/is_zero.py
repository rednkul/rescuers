from django import template

register = template.Library()

@register.filter
def is_zero(value):
    if not value:
        return ''
    else:
        return value