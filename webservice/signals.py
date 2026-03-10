from typing import Any

from constance.signals import config_updated
from django.dispatch import receiver

from .models import Layer


def _update_feature_layer_internal_visibility(old: bool, new: bool) -> None:
    if old and not new:
        # Feature is being deactivated, remove internal flag from all layers
        Layer.objects.all().update(closed_dataset=False)


@receiver(config_updated)
def config_updated(key: str, old_value: Any, new_value: Any, **kwargs) -> None:
    if key == "FEATURE_LAYER_INTERNAL_VISIBILITY":
        _update_feature_layer_internal_visibility(old_value, new_value)
