from django.core.validators import RegexValidator

no_underscore_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9-]+$',
    message='Slugs mogen alleen letters, cijfers en koppeltekens (\'-\') bevatten.',
)
