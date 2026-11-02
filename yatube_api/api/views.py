"""Вьюсеты первой версии API."""
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Group, Post

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class AuthorContentViewSet(viewsets.ModelViewSet):
    """Общие права и назначение автора для пользовательского контента."""

    permission_classes = (
        permissions.IsAuthenticated, IsAuthorOrReadOnly,
    )
    lookup_value_regex = r'\d+'

    def perform_create(self, serializer):
        """Назначить автором текущего аутентифицированного пользователя."""
        serializer.save(author=self.request.user)


class PostViewSet(AuthorContentViewSet):
    """Предоставить CRUD постов; изменять пост может только его автор."""

    queryset = Post.objects.select_related('author').order_by('id')
    serializer_class = PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Разрешить только чтение групп аутентифицированным пользователям."""

    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    lookup_value_regex = r'\d+'


class CommentViewSet(AuthorContentViewSet):
    """Предоставить CRUD комментариев внутри конкретного поста."""

    serializer_class = CommentSerializer

    def get_post(self):
        """Найти родительский пост или вернуть ответ 404."""
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Ограничить комментарии постом из адреса запроса."""
        return self.get_post().comments.select_related('author').order_by('id')

    def perform_create(self, serializer):
        """Назначить автора из токена, а родительский пост — из адреса."""
        serializer.save(author=self.request.user, post=self.get_post())
