"""Конфигурация приложения API."""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Зарегистрировать API в проекте."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
