from django import template

register = template.Library()

@register.filter(name='field_type')
def field_type(field):
    django_type = field.field.widget.__class__.__name__
    type_map = {'PasswordInput': 'password', 'TextInput': 'text', 'EmailInput': 'email'}

    if django_type in type_map.keys():
        return type_map[django_type]
    return ''