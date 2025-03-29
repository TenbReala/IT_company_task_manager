from django import template

register = template.Library()


@register.simple_tag
def active_startswith(request, starts_with_name):
    """
    Возвращает 'active', если текущий url_name начинается с переданного значения
    """
    if request.resolver_match and request.resolver_match.url_name:
        if request.resolver_match.url_name.startswith(starts_with_name):
            return "active"
    return ""
