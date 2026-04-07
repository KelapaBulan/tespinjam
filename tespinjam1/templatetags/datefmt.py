from django import template
from datetime import datetime

register = template.Library()

@register.filter
def human_date(value):
    if not value:
        return "—"
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
    except Exception:
        return value