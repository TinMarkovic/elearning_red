from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login

from forms import UserForm, CreateCourseForm
from .models import CustomUser
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



def courses(request):
    if request.method == "POST":
        #form = UserForm(request.POST)
        #if form.is_valid():
        #    new_student = CustomUser.objects.create_user(**form.cleaned_data)
        # role = Role.objects.get(name='student') 
        # role.entry_set.add(new_student)
        # login(new_student)    
        return HttpResponseRedirect('')
    elif request.method == "GET": #kasnije, nakon testiranja/impl. rola, prebaciti u drugu metodu poput PUT
        form = CreateCourseForm() 
        return render(request, 'courses.html', {'form': form}) 




