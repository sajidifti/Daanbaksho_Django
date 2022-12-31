from django.shortcuts import redirect

def donor_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None

        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'volunteer_coordinator' or group == 'volunteer':
                return redirect('home')

            if group == 'donor':
                return view_func(request, *args, **kwargs)

    return wrapper_function