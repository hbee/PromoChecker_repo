from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('items.dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper