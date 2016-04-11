from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

import models as M
import forms as F

def registration(request):
    if request.method == "POST":
        form = F.UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = F.UserForm() 

    return render(request, 'registration.html', {'form': form}) 

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
    else:
        query_results = M.Course.objects.all()
        for item in query_results:
            item.desc = (item.desc[:47] + '...') if len(item.desc) > 50 else item.desc
            item.author = (item.author[:47] + '...') if len(item.author) > 50 else item.author
            item.tagList = ""
            for tag in item.tags.all():
                item.tagList += tag.name + ", "
            
        return render(request, 'courses.html', {"query_results" : query_results})
    
    return None; # TODO: Implement display for single course


def course_manage(request, course_id):
    # Management screen for the course
    course = get_object_or_404(M.Course, id=int(course_id))
    return render(request, 'courseMng.html')

def section_modify(request, course_id, section_id=None):
    course = get_object_or_404(M.Course, id=int(course_id))
    if section_id is not None:
        section = get_object_or_404(M.Section, id=int(section_id))
    else:
        section = None
        
    if request.method == "POST":
        form = F.SectionForm(request.POST, instance=section)
        
        if form.is_valid():
            # TODO: Add the validated professor to the users - for editing
            form.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = F.SectionForm(instance=section) 
    # TODO: ADD a hidden input field with the section ID or something
        
    return render(request, 'sectionEdit.html', {'form': form}) 