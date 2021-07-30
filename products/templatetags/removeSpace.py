from django import template

register = template.Library()

@register.filter
def removeSpaceFromValue(value):
    valye= int(str(value).strip())
    return valye