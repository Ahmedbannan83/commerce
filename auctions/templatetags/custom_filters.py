from django import template

register = template.Library()

@register.filter
def get_category_count(posts, category):
    return posts.get(category, 0)
