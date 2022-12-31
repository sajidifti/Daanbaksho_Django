from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('Permission Denied')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'donor' or group == 'volunteer':
                return redirect('donorsignup')

            if group == 'admin':
                return view_func(request, *args, **kwargs)

    return wrapper_function


# Volunteer Coordinator Only
def volunteer_coordinator_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'donor' or group == 'volunteer':
                return redirect('home')

            if group == 'volunteer_coordinator':
                return view_func(request, *args, **kwargs)

    return wrapper_function