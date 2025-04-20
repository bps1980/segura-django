# utils/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from functools import wraps

def group_required(group_name):
    """Restrict view to users in a specific group."""
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)

def twofa_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('2fa_passed'):
            return redirect('twofactor_verify')
        return view_func(request, *args, **kwargs)
    return _wrapped_view