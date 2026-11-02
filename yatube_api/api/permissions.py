"""Объектные права доступа к пользовательскому контенту."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешить изменение и удаление объекта только его автору."""

    message = 'Изменять и удалять контент может только его автор.'

    def has_object_permission(self, request, view, obj):
        """Оставить чтение доступным, а запись проверить по автору."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
