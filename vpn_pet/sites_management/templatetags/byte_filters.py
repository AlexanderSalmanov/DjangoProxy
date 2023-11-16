from django import template


register = template.Library()


@register.filter(name="bytes_to_megabytes")
def bytes_to_megabytes(value):
    try:
        mb_value = value / (1024 * 1024)
        return f"{mb_value:.2f} MB"
    except (ValueError, TypeError):
        return value
