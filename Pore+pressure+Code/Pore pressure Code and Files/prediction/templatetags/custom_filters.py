from django import template

register = template.Library()

@register.filter
def confidence_color(value):
    """Return Bootstrap color class based on confidence score"""
    if value >= 0.8:
        return 'success'
    elif value >= 0.6:
        return 'warning'
    else:
        return 'danger'
