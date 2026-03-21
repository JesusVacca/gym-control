from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(role:list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return redirect('accounts:login')
            if user.is_superuser or user.is_staff:
                return func(request, *args, **kwargs)
            if user.role in role:
                return func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

