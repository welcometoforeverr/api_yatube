"""Преобразование моделей постов, групп и комментариев в JSON."""
from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    """Представить пост с именем автора и идентификатором группы."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        """Поля ответа поста."""

        model = Post
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Представить тематическую группу."""

    class Meta:
        """Поля ответа группы."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Представить комментарий с автоматически назначенными связями."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        """Поля ответа комментария и неизменяемая связь с постом."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('post',)
