from django import template

register = template.Library()

@register.filter
def filter_lesson(queryset, lesson):
    try:
        return queryset.get(lesson=lesson)
    except:
        return None 