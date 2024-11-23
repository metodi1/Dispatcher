from django import template

register = template.Library()


@register.filter
def append_to_list(value, item):
    if isinstance(value, list):
        return value + [item]  # Append item to the list and return
    return value  # Return the original value if it's not a list
