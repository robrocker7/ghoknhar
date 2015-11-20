from django import template

register = template.Library()

@register.filter(name='is_select')
def is_select(field):
    if field is None:
        return False
    return field.field.widget.__class__.__name__ == 'Select'
