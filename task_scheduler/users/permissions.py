from rest_framework import permissions
from rest_framework import request as Request


class IsUnAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return not request.user.is_authenticated
        return True
