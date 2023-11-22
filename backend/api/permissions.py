from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.IsAuthenticatedOrReadOnly):
    """Права доступа для автора."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
