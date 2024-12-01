from functools import wraps
from django.http import HttpResponseForbidden



def role_required(allowed_roles):
    """
        Custom decorator to make sure right person has access can be done by group too .
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to access this resource.")
        return _wrapped_view
    return decorator