from django import template

register = template.Library()

@register.filter
def format_price(value):
    if not value: return "$0"
    return f"${value:,.0f}".replace(",", ".")

@register.filter
def format_measures(value):
    if not value: return "0"
    return f"{value:,.1f}".replace(",", ".")