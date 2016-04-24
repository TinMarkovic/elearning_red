from django.http import HttpResponseRedirect
from .models import Role, CustomUser

def admin_only(function):
    def wrap(request, *args, **kwargs):
      
        user = CustomUser.objects.get(id=request.user.id)
        if user.role.name == 'admin':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def students_forbidden(function):
    def wrap(request, *args, **kwargs):
      
        user = CustomUser.objects.get(id=request.user.id)
        if user.role == 'student':
            return HttpResponseRedirect('/')
        else:
            return function(request, *args, **kwargs)
        
    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
"""
def admin_and_course_relates_prof(function):
    def wrap(request, *args, **kwargs):
      
        user = CustomUser.objects.get(id=request.user.id)
        if user.role.name == 'admin':
            return function(request, *args, **kwargs)
        
        elif user.role.name == 'profesor':
            
            
            return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap
"""