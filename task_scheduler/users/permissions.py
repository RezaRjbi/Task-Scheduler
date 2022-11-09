from rest_framework import permissions

class ISAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff