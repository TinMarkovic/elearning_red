from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg
from django.utils.translation import ugettext
from django.views.decorators.csrf import csrf_exempt
from json import loads
import models as M
import forms as F


def registration(request):
    if request.method == "POST":
        form = F.CustomRegistrationForm(request.POST)
        if form.is_valid():
            new_student = M.CustomUser.objects.create_user(username=form.cleaned_data['username'], first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], password=form.cleaned_data['password1'], dob=form.cleaned_data['dob'], email=form.cleaned_data['email'])
            new_student.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_student)
            return HttpResponseRedirect('')
    else:
        form = F.CustomRegistrationForm()

    return render(request, 'registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = F.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
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
        return render(request, 'courses_menu.html',
                      {"courses_inscribed": courses_inscribed, "courses_uninscribed": courses_uninscribed})
    else:
        query_results = M.Course.objects.all()
        return render(request, 'courses.html', {"query_results": query_results})


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
            for course in form.cleaned_data['courses']:
                course.programmes.add(programme)
                form.save()
        return HttpResponseRedirect('')

    else:
        form = F.ProgrammeForm(instance=programme)

    return render(request, 'registration.html', {'form': form})


def programmes_show(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
        query_results = M.Course.objects.filter(programmes=programme)
        return render(request, 'courses.html', {'query_results': query_results})
    else:
        programmes = M.Programme.objects.all()
        return render(request, 'programmes.html', {'programmes': programmes})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')


def course_manage(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    query_results = M.Section.objects.filter(course__id=course_id)
    if query_results is not None:
        return render(request, 'courseMng.html', {"query_results": query_results, "course_id": course_id})
    else:
        return render(request, 'courseMng.html', {"course_id": course_id})


#TEMP: Until we finish testing, and implement users properly
@csrf_exempt
def course_reorder_sections(request):
    course_id = request.POST['course_id']
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        section = get_object_or_404(M.Section, id=int(new_order[i]), course=int(course_id))
        section.index = i
        section.save()
    return HttpResponse('')

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
        return HttpResponseRedirect('/courses/manage/' + course_id)
    else:
        initialDict = {
            'course': course_id,
            'index': M.Section.objects.filter(course__id=course_id).count()
        }
        form = F.SectionForm(instance=section, initial=initialDict)

    return render(request, 'sectionEdit.html', {'form': form})


def section_manage(request, course_id, section_id):
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    if query_results is not None:
        return render(request, 'sectionMng.html', {"query_results": query_results,
                                                   "course_id": course_id,
                                                   "section_id": section_id,})
    else:
        return render(request, 'sectionMng.html', {"course_id": course_id,
                                                   "section_id": section_id,})


#TEMP: Until we finish testing, and implement users properly
@csrf_exempt
def section_reorder_blocks(request):
    section_id = request.POST['section_id']
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        block = get_object_or_404(M.Block, id=int(new_order[i]), sections=int(section_id))
        block.index = i
        block.save()
    return HttpResponse('')


#TEMP: Until we finish testing, and implement users properly
@csrf_exempt
def section_list_blocks(request):
    section_id = request.POST['section_id']
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    response = serialize("json", query_results.order_by("index"))
    print response
    return HttpResponse(response)

    
#TEMP: Until we finish testing, and implement users properly
@csrf_exempt
def block_modify(request, course_id, section_id, block_type=None, block_id=None):
    section = get_object_or_404(M.Section, id=int(section_id))

    if block_id is not None:
        block = get_object_or_404(M.Block, id=int(block_id))
        if hasattr(block, 'htmlblock'):
            block_type = "html";
            block = block.htmlblock
        elif hasattr(block, 'videoblock'):
            block_type = "video";
            block = block.videoblock
        elif hasattr(block, 'quizblock'):
            block_type = "quiz";
            block = block.quizblock
        elif hasattr(block, 'imageblock'):
            block_type = "quiz";
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
        print request.POST
        form = typeForm[block_type](request.POST, instance=block)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/courses/manage/' + course_id + "/section/" + section_id)
    else:
        initialDict = {
            'sections': section_id,
            'index': M.Block.objects.filter(sections__id=section_id).count()
        }
        if block is not None:
            form = typeForm[block_type](instance=block)
        else:
            form = typeForm[block_type](instance=block, initial=initialDict)
            
    if block_type == "quiz":
        return render(request, 'quizEdit.html', {'form': form, "course_id": course_id, "section_id": section_id, })
    return render(request, 'blockEdit.html', {'form': form})


def homepage(request):
    message = ugettext('Welcome to ElearningRed!')
    return render(request, 'home.html', {'message': message})


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

    return render(request, 'addstudents.html', {'form': form})


def course_details(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    return render(request, 'course_details.html', {"course": course})


def test_render(request):
    return render(request, 'quizEdit.html')