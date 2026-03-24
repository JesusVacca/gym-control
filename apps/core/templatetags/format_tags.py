from django import template
from django.utils import formats

register = template.Library()

@register.filter
def format_price(value):
    if not value: return "$0"
    return f"${value:,.0f}".replace(",", ".")

@register.filter
def format_measures(value):
    if not value: return "0"
    return f"{value:,.1f}".replace(",", ".")


@register.filter
def format_date_only(value):
    if not value: return ""
    return formats.date_format(value, "DATE_FORMAT")