from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from typing import List, Tuple
from functools import wraps

from django.db import models


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
    def get_req_and_kwarg(cls, args: tuple, kwargs: dict, kw: str):
        """
        get the request object from pos-arguments and kw from keyword-arguments from decorated functions.
        if kwargs not provided just the request object will be returned.
        we need this values to set different permissions for different users
        """
        if not kw:
            return args[1], None
        return args[1], kwargs.get(kw)

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

    @classmethod
    def is_authenticated(cls, f):
        def wrapper(*args, **kwargs):
            request = args[1]
            if bool(request.user):
                return f(*args, **kwargs)
            raise PermissionDenied

        return wrapper

    @classmethod
    def has_permission(cls, perms: List[str], kw: str = None,
                       model_filed: Tuple[models.Model, str] | str = None):
        def decorator(f):
            wraps(f)

            def wrapper(*args, **kwargs):
                request, pk = cls.get_req_and_kwarg(args, kwargs, kw)
                permission_check_list = list()
                if "is_owner" in perms:
                    if not pk:
                        raise Exception("key-word for comparison not provided")
                    if model_filed == "user":
                        if "is_staff" in perms:
                            permission_check_list.append(bool(request.user.id == pk or request.user.is_staff))
                            perms.remove("is_staff")
                        else:
                            permission_check_list.append(bool(request.user.id == pk))
                    else:
                        model, owner_field_name = model_filed
                        if not model or not owner_field_name:
                            raise Exception(
                                "model and owner_filed_name are necessary for object level permission check"
                            )
                        db_instance = get_object_or_404(model, pk=pk)
                        owner = getattr(db_instance, owner_field_name)
                        permission_check_list.append(bool(owner.id == request.user.id))
                        perms.remove("is_owner")
                for perm in perms:
                    permission_check_list.append(bool(getattr(request.user, perm)))
                if all(permission_check_list):
                    return f(*args, **kwargs)
                raise PermissionDenied
            return wrapper
        return decorator

