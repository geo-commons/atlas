from constance import config
from constance import settings as constance_settings

def get_settings(allow_settings):
    setting_list = []
    settings = constance_settings.CONFIG.items()

    for key, options in settings:
        if key in allow_settings:
            default, help_text = options[0], options[1]
            data = {'key': key,
                    'default': default,
                    'help_text': help_text,
                    'value': getattr(config, key)}
            setting_list.append(data)
    return setting_list

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def process_value(value):
    if value == "true":
        return True
    if value == "false":
        return False
    if is_float(value):
        return float(value)
    return value