from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.forms import  AuthenticationForm

from forms import UserForm, CourseForm, ProgrammeForm, LoginForm, HTMLBlockForm, RatingForm

from .models import CustomUser, Course, Rating
from .models import Role, Programme, Section, HTMLBlock
from django.db.models import Avg

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
        #form = LoginForm(request.POST)
	form = AuthenticationForm(request.POST)
	username= request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password=password)
	if user is not None:
	    if user.is_active:
	    	login(request, user)
            	return HttpResponseRedirect('')
    else:
        #form = LoginForm()   
	form = AuthenticationForm(request.POST)
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
	sections = Section.objects.filter(course_id=course.id)

	rating = Rating.objects.filter(user=request.user).filter(course=course_id)		
        if len(rating) == 0:
	    rating = Rating(user=CustomUser.objects.get(id=request.user.id), course=Course.objects.get(id=course_id))
	    rating.value = 0
	    rating.save()
        else:	
	    rating = get_object_or_404(Rating, user=CustomUser.objects.get(id=request.user.id), course=Course.objects.get(id=course_id))
	
	if request.method == "POST":
	    form = RatingForm(request.POST, instance = rating)
	    if form.is_valid():
		form.save()
		course.avgRating= Rating.objects.filter(course=course).aggregate(Avg('value')).values()[0]		
		course.save()
		
		for programme in Programme.objects.filter(course__id=course_id):
		    programme.avgRating = Course.objects.filter(programmes__name=programme).aggregate(Avg('avgRating')).values()[0]
		    programme.save()
        	return HttpResponseRedirect('') 
        	
        else: 
            form = RatingForm(instance=rating) 
	    
	return render(request, 'courses_view.html', {"sections" : sections, "form" : form, "course": course})
 	
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
        L = request.POST.getlist('courses')
        if form.is_valid():
	    for course in form.cleaned_data['courses']:
		course.programmes.add(programme)
		form.save()
        return HttpResponseRedirect('') 
        
    else: 
        form = ProgrammeForm(instance=programme) 
    

    return render(request, 'registration.html', {'form': form}) 

def programmes_show(request, programme_id=None):
    print [choice.name for choice in Course.objects.all()]
    if programme_id is not None:
	programme = get_object_or_404(Programme, id=int(programme_id))
	query_results = Course.objects.filter(programmes=programme)
	return render(request, 'courses.html', {'query_results' : query_results})
    else:
    	programmes = Programme.objects.all()
	return render(request, 'programmes.html', {'programmes' : programmes})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def HTMLBlock_modify(request, HTMLBlock_id=None):
    if HTMLBlock_id is not None:
        block = get_object_or_404(HTMLBlock, id=int(HTMLBlock_id))
    else:
        block = None

    if request.method == "POST":
        form = HTMLBlockForm(request.POST, instance=block)
        
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = HTMLBlockForm(instance=block) 
        
    return render(request, 'HTMLBlock_edit.html', {'form': form})

def HTMLBlock_show(request, HTMLBlock_id=None):
    if HTMLBlock_id is not None:
	print (HTMLBlock_id)
    else:
	htmlBlocks = HTMLBlock.objects.all()
	return render(request, 'HTMLBlock.html', {'htmlBlocks' : htmlBlocks})

