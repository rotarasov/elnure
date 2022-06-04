from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ElnureConfigConfig(AppConfig):
    name = "elnure_config"
    verbose_name = _("Configuration")
