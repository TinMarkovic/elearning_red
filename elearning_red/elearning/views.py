from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from forms import UserForm, CourseForm
from .models import CustomUser, Course
from .models import Role

def registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_student = CustomUser.objects.create_user(**form.cleaned_data)
  
	  # role = Role.objects.get(name='student') 
	  # role.entry_set.add(new_student)
	    
	  # login(new_student)
            
            return HttpResponseRedirect('')
    else:
        form = UserForm() 

    return render(request, 'registration.html', {'form': form}) 



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
        
        print "Course created!" #Debug za konzole :)
        return HttpResponseRedirect('') #TODO dodati homepage/listu courseova
        
    else: 
        form = CourseForm(instance=course) 
        
    return render(request, 'courses.html', {'form': form}) 
