from django import template
import mistune
from mistune.directives import DirectiveToc

register = template.Library()

@register.filter
def markdown(value):
    markdown = mistune.create_markdown(
        plugins=[DirectiveToc()]
    )

    return markdown(value)
