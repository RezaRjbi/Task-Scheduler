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

    def has_permission(self, request, view):
        requested_id = int(request.path.split("/")[-2])
        if request.method == "GET":
            return bool(
                request.user and (request.user.is_staff or request.user.id == requested_id)
            )
        if request.method == "PUT":
            return bool(
                request.user and request.user.id == requested_id
            )
        if request.method == "DELETE":
            return bool(
                request.user and request.user.is_staff
            )


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
