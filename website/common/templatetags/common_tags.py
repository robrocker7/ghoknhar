from django import template
import hashlib

register = template.Library()

@register.filter(name='is_select')
def is_select(field):
    if field is None or field is '':
        return False
    print 'Field: {0}'.format(field)
    return field.field.widget.__class__.__name__ == 'Select'


@register.filter(name='md5')
def md5(text):
    if text is None:
        return False
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()
