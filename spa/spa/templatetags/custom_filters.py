# spa/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def has_attr(obj, attr_name):
    """
    Devuelve True si `obj` tiene el atributo `attr_name`.
    Ejemplo de uso en plantilla:
      {% if user|has_attr:"profesional" %}
    """
    return hasattr(obj, attr_name)
