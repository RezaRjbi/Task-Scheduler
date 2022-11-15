from rest_framework import permissions


class IsAdminOrNewUser(permissions.BasePermission):
    """
    allow admins to get a list of all users and allow everyone to register
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user and request.user.is_staff)
        return True


class IsAdminOrOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and (request.user.is_staff or request.user.id == obj.id)
        )
