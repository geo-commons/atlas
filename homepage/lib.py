from os import path
from django.conf import settings


def get_help_content():
    filename = path.join(settings.BASE_DIR, 'docs', 'help.md')
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()
