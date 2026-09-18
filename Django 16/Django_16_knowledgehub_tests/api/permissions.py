from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.status == 'published'
        return obj.author == request.user