from rest_framework.exceptions import PermissionDenied

from django.shortcuts import get_object_or_404
from django.db import models

from typing import List, Tuple
from functools import wraps

from utils.permissions import get_req_and_kwarg
from . import filters


def has_permission(perms: List[str], kw: str = None,
                   model_filed: Tuple[models.Model, str] | str = None):
    """
    main permission function for providing permission for each view and request.
    """
    def decorator(f):
        wraps(f)

        def wrapper(*args, **kwargs):
            request, pk = get_req_and_kwarg(args, kwargs, kw)
            permission_check_list = dict()
            if filters.IS_OWNER in perms:
                if not pk:
                    raise Exception("key-word for comparison not provided")
                if model_filed == "User":
                    permission_check_list["is_owner"] = bool(request.user.id == pk)
                else:
                    model, owner_field_name = model_filed
                    if not model or not owner_field_name:
                        raise Exception(
                            "model and owner_filed_name are necessary for object level permission check"
                        )
                    db_instance = get_object_or_404(model, pk=pk)
                    owner = getattr(db_instance, owner_field_name)
                    permission_check_list["is_owner"] = bool(owner.id == request.user.id)
            for perm in perms:
                if perm == filters.IS_OWNER:
                    continue
                permission_check_list[perm] = bool(getattr(request.user, perm))

            # if is_owner is in required permissions, and it is False, we are going to check if there is
            # is_staff or is_superuser. so if we use this two filters with other filters, it's going to override them.

            if filters.IS_OWNER in perms:
                # if user is not owner we check for admin privilege
                if not permission_check_list.get(filters.IS_OWNER):
                    if permission_check_list.get(filters.IS_STAFF) or permission_check_list.get(filters.IS_SUPERUSER):
                        # if user is admin it has precedence over is_owner
                        return f(*args, **kwargs)
                    # not owner and not staff
                    raise PermissionDenied
                # is owner
                return f(*args, **kwargs)
            # object level permission level not required
            if all(permission_check_list.values()):
                return f(*args, **kwargs)
            raise PermissionDenied

        return wrapper

    return decorator
