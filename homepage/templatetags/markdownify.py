from django import template
import mistune
from mistune.directives import FencedDirective, TableOfContents

register = template.Library()


@register.filter
def markdown(value):
    markdown = mistune.create_markdown(plugins=[
        FencedDirective([
            TableOfContents()
        ])
    ])

    return markdown(value)
