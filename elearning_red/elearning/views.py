from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404

import models as M
import forms as F

def registration(request):
    if request.method == "POST":
        form = F.UserForm(request.POST)
    if form.is_valid():
            new_student = M.CustomUser.objects.create_user(**form.cleaned_data)
            new_student.backend = 'django.contrib.auth.backends.ModelBackend'        
            login(request, new_student)
            return HttpResponseRedirect('')
    else:
        form = F.UserForm() 

    return render(request, 'registration.html', {'form': form}) 


def user_login(request):
    if request.method == "POST":
        form = F.LoginForm(request.POST)
        username= request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('')
    else:
        form = F.LoginForm()   

    return render(request, 'index.html', {'form': form})

def course_modify(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
    else:
        course = None
        
    if request.method == "POST":
        form = F.CourseForm(request.POST, instance=course)
        
        if form.is_valid():
            # TODO: Add the validated professor to the users - for editing
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = F.CourseForm(instance=course) 
        
    return render(request, 'course.html', {'form': form}) 

def course_show(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
        sections = M.Section.objects.filter(course_id=course.id)
        return render(request, 'courses_view.html', {"sections" : sections})

    elif request.user.is_authenticated():
        courses_inscribed = M.Course.objects.filter(users=request.user.id)
        courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
        return render(request, 'courses_menu.html', {"courses_inscribed" : courses_inscribed, "courses_uninscribed" : courses_uninscribed})
    else:    	
        query_results = M.Course.objects.all()
        return render(request, 'courses.html', {"query_results" : query_results})
 
def user_modify(request, customUser_id=None):
    if customUser_id is not None:
        customUser = get_object_or_404(M.CustomUser, id=int(customUser_id))
    else:
        customUser = None
        
    if request.method == "POST":
        form = F.UserForm(request.POST)
        
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = F.UserForm(instance=customUser) 
        
    return render(request, 'registration.html', {'form': form}) 

def programme_modify(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
    else:
        programme = None
        
    if request.method == "POST":
        form = F.ProgrammeForm(request.POST, instance=programme)
        
        if form.is_valid():
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = F.ProgrammeForm(instance=programme) 
        
    return render(request, 'registration.html', {'form': form}) 

def programmes_show(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
        query_results = M.Course.objects.filter(programmes=programme)
        return render(request, 'courses.html', {'query_results' : query_results})
    else:
        programmes = M.Programme.objects.all()
        return render(request, 'programmes.html', {'programmes' : programmes})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def course_manage(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    query_results = M.Section.objects.filter(course__id=course_id)
    if query_results is not None:
        return render(request, 'courseMng.html', {"query_results" : query_results, "course_id" : course_id})
    else:
        return render(request, 'courseMng.html', {"course_id" : course_id})

def section_modify(request, course_id, section_id=None):
    course = get_object_or_404(M.Course, id=int(course_id))
    if section_id is not None:
        section = get_object_or_404(M.Section, id=int(section_id))
    else:
        section = None
 
    if request.method == "POST":
        form = F.SectionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/courses/manage/'+course_id) 
    else: 
        initialDict = {
               'course': course_id,
               'index': M.Section.objects.filter(course__id=course_id).count() 
               }
        form = F.SectionForm(instance=section, initial=initialDict) 
        
    return render(request, 'sectionEdit.html', {'form': form})

def section_manage(request,course_id, section_id):
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    if query_results is not None:
        return render(request, 'sectionMng.html', {"query_results" : query_results, 
                                                   "course_id" : course_id,
                                                   "section_id" : section_id,})
    else:
        return render(request, 'sectionMng.html', {"course_id" : course_id,
                                                   "section_id" : section_id,}) #temporary
    
def block_modify(request, course_id, section_id, block_type="html", block_id=None):
    section = get_object_or_404(M.Section, id=int(section_id))
    
    if block_id is not None:
        block = get_object_or_404(M.Block, id=int(block_id))
        if hasattr(block, 'htmlblock'):
            block = block.htmlblock
        elif hasattr(block, 'videoblock'):
            block = block.videoblock
        elif hasattr(block, 'quizblock'):
            block = block.quizblock
        elif hasattr(block, 'imageblock'):
            block = block.imageblock
    else:
        block = None

    typeForm = {
                'html': F.HTMLBlockForm,
                'video': F.VideoBlockForm,
                'image': F.ImageBlockForm,
                'quiz': F.QuizBlockForm,
                }
    
    if request.method == "POST":
        form = typeForm[block_type](request.POST, instance=block)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/courses/manage/'+course_id+"/section/"+section_id) 
    else: 
        initialDict = {
               'sections': section_id,
               'index': M.Block.objects.filter(sections__id=section_id).count() 
                }
        form = typeForm[block_type](instance=block, initial=initialDict) 
        
    return render(request, 'blockEdit.html', {'form': form})
