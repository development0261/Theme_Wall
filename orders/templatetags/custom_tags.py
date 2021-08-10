from django import template

register = template.Library()


@register.filter
def subtract(value, tax):
    return float(value) - float(tax)

@register.filter
def multiply(qty, unit_price, *args, **kwargs):
    return qty * unit_price