# my_filters.py

from django import template
from datetime import datetime

register = template.Library()

@register.filter
def split_message(value):
    parts = value.split(' - ')
    date = datetime.fromisoformat(parts[0])
    formatted_date = date.strftime("%b %d, %Y %I:%M%p")
    sender = parts[1]
    message = parts[2]
    return formatted_date, sender, message
