from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to access/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Only allow owners of the note to access it
        return obj.author == request.user
