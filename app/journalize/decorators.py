from django.http import HttpResponseRedirect


def logged_in_redirect(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/entry/')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap