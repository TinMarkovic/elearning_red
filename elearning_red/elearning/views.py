from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from datetime import datetime

from forms import UserForm, CourseForm, ProgrammeForm, LoginForm

from .models import CustomUser, Course
from .models import Role, Programme, Section

def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        #TODO:check if admin or student
	if form.is_valid():
            new_student = CustomUser.objects.create_user(**form.cleaned_data)
	    new_student.backend = 'django.contrib.auth.backends.ModelBackend'	    
	    login(request, new_student)
            
            return HttpResponseRedirect('')

    else:
        form = UserForm() 

    return render(request, 'registration.html', {'form': form}) 


def user_login(request):
    if request.method == "POST":
        username= request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password=password)

        return HttpResponseRedirect('')
    else:
        form = LoginForm()   

    return render(request, 'index.html', {'form': form})


def course_modify(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(Course, id=int(course_id))
    else:
        course = None
        
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        
        if form.is_valid():
            # TODO: Add the validated professor to the users - for editing
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = CourseForm(instance=course) 
        
    return render(request, 'course.html', {'form': form}) 

def course_show(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(Course, id=int(course_id))
	query_results = Section.objects.filter(course_id=course.id)
        return render(request, 'courses.html', {"query_results" : query_resluts})

    elif request.user.is_authenticated():
        courses_inscribed = Course.objects.filter(users=request.user.id)
	courses_uninscribed = Course.objects.exclude(users=request.user.id)
        return render(request, 'courses_menu.html', {"courses_inscribed" : courses_inscribed, "courses_uninscribed" : courses_uninscribed})
    else:    	
	query_results = Course.objects.all()
        return render(request, 'courses.html', {"query_results" : query_results})
 
def user_modify(request, customUser_id=None):
    if customUser_id is not None:
        customUser = get_object_or_404(CustomUser, id=int(customUser_id))
    else:
        customUser = None
        
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = UserForm(instance=customUser) 
        
    return render(request, 'registration.html', {'form': form}) 

def programme_modify(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(Programme, id=int(programme_id))
    else:
        programme = None
        
    if request.method == "POST":
        form = ProgrammeForm(request.POST, instance=programme)
        
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = ProgrammeForm(instance=programme) 
        
    return render(request, 'registration.html', {'form': form}) 

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

