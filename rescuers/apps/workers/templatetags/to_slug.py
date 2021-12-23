from django import template

register = template.Library()


@register.simple_tag
def to_slug(division_id, post_id):
    return f'{division_id}_{post_id}'