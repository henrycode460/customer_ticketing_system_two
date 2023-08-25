from django import template
from urllib.parse import unquote_plus

register = template.Library()

@register.filter
def extract_filename(url):
    filename = unquote_plus(url).split('/')[-1]
    return filename