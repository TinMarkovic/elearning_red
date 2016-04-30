from django.apps import AppConfig
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import decorators as D
from json import loads
import models as M
import forms as F

def registration(request):
    if request.method == "POST":
        form = F.CustomRegistrationForm(request.POST)
        if form.is_valid():
            new_student = M.CustomUser.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password1'], dob=form.cleaned_data['dob'], email=form.cleaned_data['email'], role=M.Role.objects.get(name='student'))
            new_student.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_student)
            return HttpResponseRedirect('/')
    else:
        form = F.CustomRegistrationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


def homepage(request):
    message = ugettext('Welcome to ElearningRed!')
    if request.user.is_authenticated():
        courses_inscribed = M.Course.objects.filter(users=request.user.id)
        courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
        return render(request, 'home.html',
                      {'message': message,"courses_inscribed": courses_inscribed, "courses_uninscribed": courses_uninscribed})
    else:
        query_results = M.Course.objects.all()
        return render(request, 'home.html', {'message': message, "query_results": query_results})


def about(request):
    return render(request, 'about.html')


#@login_required
#@D.admin_only
def user_create(request):
    users = M.CustomUser.objects.all()
    if request.method == "POST":
        form = F.CustomRegistrationFormAdmin(request.POST)
        if form.is_valid():
            new_student = M.CustomUser.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password1'], dob=form.cleaned_data['dob'], email=form.cleaned_data['email'], role=M.Role.objects.get(name=form.cleaned_data['role']))
            return HttpResponseRedirect('')
    else:
        form = F.CustomRegistrationFormAdmin()

    return render(request, 'registration.html', {'form': form, 'users': users})

#@login_required
#@D.admin_only
def user_modify(request, customUser_id=None):
    if customUser_id is not None:
        customUser = get_object_or_404(M.CustomUser, id=int(customUser_id))
    else:
        customUser = None
        return HttpResponseRedirect('/')
    
    if request.method == "DELETE":
        if customUser is not None:
            customUser.delete()
            return HttpResponseRedirect('/users')  
        else:
            raise Http404("User does not exist")
    
    if request.method == "POST":
        form = F.UserForm(request.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect('')

    else:
        form = F.UserForm(instance=customUser)

    return render(request, 'registration.html', {'form': form})


def users_list(request):
    users = M.CustomUser.objects.all()
    
    if request.method == "DELETE":
        if customUser is not None:
            customUser.delete()
            return HttpResponse('Success!')
        else:
            raise Http404("User does not exist")

        return HttpResponseRedirect('')

    return render(request, 'users.html', {'users': users})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


#@login_required
#@D.admin_or_course_related_prof
def course_modify(request, course_id=None):
    courses = M.Course.objects.all()
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
    else:
        course = None
    if request.method == "DELETE":
        if course is not None:
            course.delete()
            return HttpResponse('')
        else:
            raise Http404("Course does not exist")
    if request.method == "POST":
        form = F.CourseForm(request.POST, instance=course)
        if form.is_valid():
            # TODO: Add the validated professor to the users - for editing
            form.save()
        return HttpResponseRedirect('')
    else:
        form = F.CourseForm(instance=course)

    return render(request, 'courseEdit.html', {'form': form, 'courses': courses})


def course_show(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
        sections = M.Section.objects.filter(course_id=course.id)
        rating = M.Rating.objects.filter(user=request.user).filter(course=course_id)
        if len(rating) == 0:
            rating = M.Rating(user=M.CustomUser.objects.get(id=request.user.id),
                              course=M.Course.objects.get(id=course_id))
            rating.value = 0
            rating.save()
        else:
            rating = get_object_or_404(M.Rating, user=M.CustomUser.objects.get(id=request.user.id),
                                       course=M.Course.objects.get(id=course_id))
        
        
        if request.method == "POST":
            form = F.RatingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                course.avgRating = M.Rating.objects.filter(course=course).aggregate(Avg('value')).values()[0]
                course.save()

                for programme in M.Programme.objects.filter(course__id=course_id):
                    programme.avgRating = M.Course.objects.filter(programmes__name=programme).aggregate(Avg('avgRating')).values()[0]
                    programme.save()
                return HttpResponseRedirect('')
        else:
            form = F.RatingForm(instance=rating)
            
        return render(request, 'courses_view.html', {"sections": sections, "form": form, "course": course})

    elif request.user.is_authenticated():
        courses_inscribed = M.Course.objects.filter(users=request.user.id)
        courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
        return render(request, 'courses.html',
                      {"courses_inscribed": courses_inscribed, "courses_uninscribed": courses_uninscribed})
    else:
        courses_uninscribed = M.Course.objects.all()
        return render(request, 'courses.html', {"courses_uninscribed": courses_uninscribed})


#@login_required
#@D.admin_or_course_related_prof
def course_manage(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    query_results = M.Section.objects.filter(course__id=course_id)
    if query_results is not None:
        return render(request, 'courseMng.html', {"query_results": query_results, "course":course})
    else:
        return render(request, 'courseMng.html', {"course":course})


#@login_required
#@D.admin_or_course_related_prof
def course_reorder_sections(request, course_id):
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        section = get_object_or_404(M.Section, id=int(new_order[i]), course=int(course_id))
        section.index = i
        section.save()
    return HttpResponse('')


#@login_required
#@D.admin_or_course_related_prof
def course_students(request, course_id):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
    else:
        course = None
    if request.method == "POST":
        form = F.StudentToCourse(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            # TODO: Add the validated professor to the users - for editing
            course.save()
        return HttpResponseRedirect('')
    else:
        form = F.StudentToCourse(instance=course)

    return render(request, 'courseStudentList.html', {'form': form,'course':course})


#@login_required
#@D.admin_only
def programme_modify(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
    else:
        programme = None
    programmes = M.Programme.objects.all()
    
    if request.method == "DELETE":
        if programme is not None:
            programme.delete()
            return HttpResponse('Success!')
        else:
            raise Http404("Programme does not exists!")
    
    if request.method == "POST":
        form = F.ProgrammeForm(request.POST, instance=programme)
    
        if form.is_valid():
            form.save()
            
        return HttpResponseRedirect('')

    else:
        form = F.ProgrammeForm(instance=programme)

    return render(request, 'programmeEdit.html', {'form': form, 'programmes': programmes})

                            
def programmes_show(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
        query_results = M.Course.objects.filter(programmes=programme)
        return render(request, 'courses.html', {'query_results': query_results})
    else:
        programmes = M.Programme.objects.all()
        return render(request, 'programmes.html', {'programmes': programmes})


#@login_required
#@D.admin_or_course_related_prof
def section_modify(request, course_id, section_id=None):
    course = get_object_or_404(M.Course, id=int(course_id))
    if section_id is not None:
        section = get_object_or_404(M.Section, id=int(section_id))
    else:
        section = None
    if request.method == "DELETE":
        if section is not None:
            section.delete()
            return HttpResponse('Success!')
        else:
            raise Http404("Section does not exist")
    if request.method == "POST":
        form = F.SectionForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('elearning:manageCourse', kwargs={'course_id': course_id}))
    else:
        initialDict = {
            'course': course_id,
            'index': M.Section.objects.filter(course__id=course_id).count()
        }
        form = F.SectionForm(instance=section, initial=initialDict)

    return render(request, 'sectionEdit.html', {'form': form, 'course':course, 'section':section})


#@login_required
#@D.admin_or_course_related_prof
def section_manage(request, course_id, section_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    if query_results is not None:
        return render(request, 'sectionMng.html', {"query_results": query_results,
                                                   "course_id": course_id,
                                                   "section_id": section_id,
                                                   "course":course,
                                                   "section":section,})
    else:
        return render(request, 'sectionMng.html', {"course_id": course_id,
                                                   "section_id": section_id,})


#@login_required
#@D.admin_or_course_related_prof
def section_reorder_blocks(request, section_id):
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        block = get_object_or_404(M.Block, id=int(new_order[i]), sections=int(section_id))
        block.index = i
        block.save()
    return HttpResponse('')


#@login_required
#@D.admin_or_course_related_prof
def section_list_blocks(request, section_id):
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    response = serialize("json", query_results.order_by("index"))
    print response
    return HttpResponse(response)


def section_studentview(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    courses_inscribed = M.Course.objects.filter(users=request.user.id)
    courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
    query_results = M.Section.objects.filter(course__id=course_id)
    if query_results is not None:
        return render(request, 'courseShow.html', {"query_results": query_results, "course_id": course_id, "course": course, "courses_inscribed": courses_inscribed, "courses_uninscribed": courses_uninscribed})
    else:
        return render(request, 'courseShow.html', {"course_id": course_id})


#@login_required
#@D.admin_or_course_related_prof
def block_modify(request, course_id, section_id, block_type=None, block_id=None):
    section = get_object_or_404(M.Section, id=int(section_id))
    if block_id is not None:
        try:
            block = M.Block.objects.get_subclass(id=int(block_id))
        except M.Block.DoesNotExist:
            raise Http404("The object does not exist.")
        block_type = type(block).__name__
        formClass = getattr(F, block_type+"Form")
    else:
        block = None
        formClass = getattr(F, block_type+"BlockForm")
    if request.method == "DELETE":
        if block is not None:
            block.delete()
            return HttpResponse('Successfully deleted.')
        else:
            raise Http404("Section does not exist")
    if request.method == "POST":
        form = formClass(request.POST, request.FILES, instance=block)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('elearning:manageSection', kwargs={'course_id': course_id, 'section_id': section_id}))
    else:
        initialDict = {
            'sections': section_id,
            'index': M.Block.objects.filter(sections__id=section_id).count()
        }
        if block is not None:
            form = formClass(instance=block)
        else:
            form = formClass(instance=block, initial=initialDict)
            
    return form.getRender(request, course_id, section_id)


def blocks_studentview(request, course_id, section_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    section = get_object_or_404(M.Section, id=int(section_id))
    blocks = M.Block.objects.filter(sections__id=section_id).select_subclasses()
    
    for block in blocks:
        block.type = type(block).__name__
    
    return render(request, 'sectionShow.html', {"course_id": course_id,
                                            "section": section,
                                            "blocks": blocks})


