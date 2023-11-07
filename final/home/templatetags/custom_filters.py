from django import template

register = template.Library()

@register.filter
def get_range(value):
    return range(value)

@register.filter
def mul(value, arg):
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''