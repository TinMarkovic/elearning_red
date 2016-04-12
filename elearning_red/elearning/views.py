from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime


from forms import UserForm, CourseForm, LoginForm
from .models import CustomUser, Course
from .models import Role

def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # bilo je, (mozda modificirati koristeci): form.save()
            new_student = CustomUser.objects.create_user(**form.cleaned_data)
            r = Role.objects.get(name="student")
            new_student.role = r
            new_student.save()
            new_student = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_student)
        # login(new_student)            
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
    else:
        query_results = Course.objects.all()
        return render(request, 'courses.html', {"query_results" : query_results})
    return None; # TODO: Implement display for single course

