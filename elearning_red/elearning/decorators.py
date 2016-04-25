from django.http import HttpResponseRedirect
from .models import Role, CustomUser, Course
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

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

def admin_or_professor(function):
    def wrap(request, *args, **kwargs):
      
        user = CustomUser.objects.get(id=request.user.id)
        if user.role.name == 'admin' | user.role.name == 'professor':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def admin_or_course_related_prof(function):
    def wrap(request, course_id=None, *args, **kwargs):
        if course_id is not None:
            user = CustomUser.objects.get(id=request.user.id)
            if user.role.name == 'admin':
                return function(request, course_id, *args, **kwargs)
            elif user.role.name == 'professor':
                course = get_object_or_404(Course, id=int(course_id))
                try:
                    course = Course.objects.get(id=course_id,users=user)
                    return function(request, course_id, *args, **kwargs)
                
                except ObjectDoesNotExist:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/')
        else: 
            if user.role.name == 'admin' | user.role.name == 'profesor':
                return function(request, course_id, *args, **kwargs)
            else:
                return HttpResponseRedirect('/')

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

def admin_or_course_related_prof_or_student(function):
    def wrap(request, course_id=None, *args, **kwargs):
        if course_id is not None:
            user = CustomUser.objects.get(id=request.user.id)
            if user.role.name == 'admin':
                return function(request, course_id, *args, **kwargs)
            elif user.role.name == 'professor' | user.role.name == 'student':
                course = get_object_or_404(Course, id=int(course_id))
                try:
                    course = Course.objects.get(id=course_id,users=user)
                    return function(request, course_id, *args, **kwargs)
                
                except ObjectDoesNotExist:
                    return HttpResponseRedirect('/')
                
            else:
                return HttpResponseRedirect('/')
               
        else:
            return function(request, course_id, *args, **kwargs)
            

    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap

