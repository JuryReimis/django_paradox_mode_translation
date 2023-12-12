from django.template import Library

register = Library()


@register.filter
def get_model_name(value):
    return value.__class__.__name__
