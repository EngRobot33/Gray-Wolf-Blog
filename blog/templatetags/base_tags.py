from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def home():
    return "صفحه اصلی"

@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category" : Category.objects.filter(status=True)
    }