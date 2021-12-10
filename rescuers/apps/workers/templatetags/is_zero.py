from django import template

register = template.Library()

@register.filter
def is_zero(value):
    if value == 0:
        return ''
    else:
        return value