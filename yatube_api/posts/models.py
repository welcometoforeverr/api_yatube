"""Модели контента социальной сети."""
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    """Тематическая группа публикаций."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        """Вернуть название группы."""
        return self.title


class Post(models.Model):
    """Публикация пользователя с необязательной группой и изображением."""

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )  # поле для картинки
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    def __str__(self):
        """Вернуть текст публикации."""
        return self.text


class Comment(models.Model):
    """Комментарий пользователя к публикации."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
