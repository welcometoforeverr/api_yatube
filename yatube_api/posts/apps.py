"""Конфигурация приложения публикаций."""
from django.apps import AppConfig


class PostsConfig(AppConfig):
    """Зарегистрировать приложение публикаций."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
