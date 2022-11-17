from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsAdminOrNewUser(permissions.BasePermission):
    """
    allow admins to get a list of all users and allow everyone to register
    """

    def has_permission(self, request, view):
        if request.method == "GET":
            return bool(request.user and request.user.is_staff)
        return True


class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class CustomPermissions:
    @classmethod
    def get_req_and_kwarg(cls, args: tuple, kwargs: dict, kw: str, convert_to_int: bool = True):
        """
        get the request object from pos-arguments and kw from keyword-arguments from decorated functions.
        we need this values to set different permissions for different users
        """
        value = kwargs.get(kw)
        if convert_to_int:
            int(value)
        return args[1], value

    @classmethod
    def is_admin_or_owner(cls, f):
        def wrapper(*args, **kwargs):
            request, pk = cls.get_req_and_kwarg(args, kwargs, "pk")
            if bool(request.user and (request.user.id == pk or request.user.is_staff)):
                return f(*args, **kwargs)
            raise PermissionDenied

        return wrapper

    @classmethod
    def is_owner(cls, f):
        def wrapper(*args, **kwargs):
            request, pk = cls.get_req_and_kwarg(args, kwargs, "pk")

            if bool(request.user and request.user.id == pk):
                return f(*args, **kwargs)
            raise PermissionDenied

        return wrapper

    @classmethod
    def is_admin(cls, f):
        # todo: make this decorator usable for views that has no "pk"
        def wrapper(*args, **kwargs):
            request, pk = cls.get_req_and_kwarg(args, kwargs, "pk")

            if bool(request.user and request.user.is_staff):
                return f(*args, **kwargs)
            raise PermissionDenied

        return wrapper
