from django import template
from django.template.defaultfilters import stringfilter
from bs4 import BeautifulSoup

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def tailwinds(value):
    soup = BeautifulSoup(value, "html.parser")

    for t in soup.find_all("p"):
        t["class"] = "mb-4"
    
    for t in soup.find_all("h2"):
        t["class"] = "my-2 font-semibold"

    return str(soup)
