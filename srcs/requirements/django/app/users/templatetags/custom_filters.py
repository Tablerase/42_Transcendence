from django import template

register = template.Library()

@register.filter(name='reverse_list')
def reverse_list(value):
    return reversed(value)
