from django import template

register = template.Library()


@register.filter
def split_skills(value):
    """Split a comma-separated skills string into a list of stripped strings."""
    if not value:
        return []
    return [s.strip() for s in value.split(',') if s.strip()]


@register.filter
def trim(value):
    """Strip whitespace from a string."""
    if value is None:
        return ''
    return str(value).strip()
