from django.apps import AppConfig
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
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
            new_student = M.CustomUser.objects.create_user(username=form.cleaned_data['username'],
                                 first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'],
                                 password=form.cleaned_data['password1'], dob=form.cleaned_data['dob'], 
                                 email=form.cleaned_data['email'], role=M.Role.objects.get(name='student'))
            new_student.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, new_student)
            return HttpResponseRedirect(reverse('elearning:homepage'))
    else:
        form = F.CustomRegistrationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


def homepage(request):
    message = ugettext('Welcome to ElearningRed!')
    if request.user.id: 
        customUser = get_object_or_404(M.CustomUser, id=int(request.user.id))
        request.session['customUserRole'] = customUser.getRole
    if request.user.is_authenticated():
        courses_inscribed = M.Course.objects.filter(users=request.user.id)
        courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
        return render(request, 'home.html',
                      {'message': message,"courses_inscribed": courses_inscribed,
                        "courses_uninscribed": courses_uninscribed})
    else:
        query_results = M.Course.objects.all()
        return render(request, 'home.html', {'message': message, "query_results": query_results})


def about(request):
    return render(request, 'about.html')


@login_required 
@D.admin_only
def user_create(request):
    users = M.CustomUser.objects.all()
    if request.method == "POST":
        form = F.CustomRegistrationFormAdmin(request.POST)
        if form.is_valid():
            new_student = M.CustomUser.objects.create_user(username=form.cleaned_data['username'], 
                                first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name'], 
                                password=form.cleaned_data['password1'], dob=form.cleaned_data['dob'], 
                                email=form.cleaned_data['email'], role=M.Role.objects.get(name=form.cleaned_data['role']))
            return HttpResponseRedirect(reverse('elearning:listUsers'))
    else:
        form = F.CustomRegistrationFormAdmin()

    return render(request, 'registration.html', {'form': form, 'users': users})

@login_required
@D.admin_only
def user_modify(request, customUser_id=None):
    if customUser_id is not None:
        customUser = get_object_or_404(M.CustomUser, id=int(customUser_id))
    else:
        return HttpResponseRedirect(reverse('elearning:createUser'))
    
    if request.method == "DELETE":
        if customUser is not None:
            customUser.delete()
            return HttpResponse('Success, user deleted.')  
        else:
            raise Http404("User does not exist")
    
    if request.method == "POST":
        form = F.UserForm(request.POST, instance=customUser)
        
        if form.is_valid():
            form.save()
           
        return HttpResponseRedirect(reverse('elearning:listUsers'))

    else:
        form = F.UserForm(instance=customUser)

    return render(request, 'registration.html', {'form': form})


def users_list(request):
    users = M.CustomUser.objects.all()
    return render(request, 'users.html', {'users': users})


@login_required
def user_profile(request):
    return render(request, 'userProfile.html')
    
@login_required
@D.admin_or_course_related_prof
def course_modify(request, course_id=None):
    courses = M.Course.objects.all()
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
    else:
        course = None
    if request.method == "DELETE":
        if course is not None:
            course.delete()
            return HttpResponse('Success. Course deleted.')
        else:
            raise Http404("Course does not exist")
    if request.method == "POST":
        form = F.CourseForm(request.POST, instance=course)
        if form.is_valid():
            model = form.save()
            model.users.add(get_object_or_404(M.CustomUser, id=int(request.user.id)))
        return HttpResponseRedirect(reverse('elearning:manageCourse', kwargs={'course_id': course_id}))
    else:
        form = F.CourseForm(instance=course)

    return render(request, 'courseEdit.html', {'form': form, 'courses': courses})


@D.admin_or_course_related_prof_or_student
def course_show(request, course_id=None):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
        sections = M.Section.objects.filter(course_id=course.id)
        """
        try:
            rating = M.Rating.objects.get(user=request.user, course=course_id)
        except ObjectDoesNotExist:
            rating = M.Rating(value=0, user=M.CustomUser.objects.get(id=request.user.id),
                              course=M.Course.objects.get(id=course_id))
            rating.save()
          
        if request.method == "POST":
            form = F.RatingForm(request.POST, instance=rating)
            if form.is_valid():
                form.save()
                course.avgRating = M.Rating.objects.filter(course=course).aggregate(Avg('value')).values()[0]
                course.save()

                for programme in M.Programme.objects.filter(course__id=course_id):
                    programme.avgRating = M.Course.objects.filter(programmes__name=programme).aggregate(Avg('avgRating')).values()[0]
                    programme.save()
                return HttpResponseRedirect(reverse('elearning:showCourse', kwargs={'course_id': course_id}))
        else:
            form = F.RatingForm(instance=rating)
        """    
        return render(request, 'courseShow.html', {"sections": sections, "course": course, "course_id": course_id})

    elif request.user.is_authenticated():
        courses_inscribed = M.Course.objects.filter(users=request.user.id)
        courses_uninscribed = M.Course.objects.exclude(users=request.user.id)
        return render(request, 'courses.html',
                      {"courses_inscribed": courses_inscribed, "courses_uninscribed": courses_uninscribed})
    else:
        courses_uninscribed = M.Course.objects.all()
        return render(request, 'courses.html', {"courses_uninscribed": courses_uninscribed})


@login_required
@D.admin_or_course_related_prof
def course_manage(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    query_results = M.Section.objects.filter(course__id=course_id)
    if query_results is not None:
        return render(request, 'courseMng.html', {"query_results": query_results, "course":course})
    else:
        return render(request, 'courseMng.html', {"course":course })


@login_required
@D.admin_or_course_related_prof
def course_reorder_sections(request, course_id):
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        section = get_object_or_404(M.Section, id=int(new_order[i]), course=int(course_id))
        section.index = i
        section.save()
    return HttpResponse('Success')


@D.admin_or_course_related_prof_or_student
def course_rating(request, course_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    if request.method == "POST":
        rating = int(request.POST['rating'])
        ratingObj = M.Rating.create(rating, request.user, course)
        ratingObj.save()
        return HttpResponse('Success')
    if request.method == "GET":
        ratingObj = M.Rating.objects.filter(course__id=course.id).filter(user__id=request.user.id)
        if not ratingObj:
            return HttpResponse(0)
        rating = ratingObj[0].value
        return HttpResponse(rating)


@login_required
@D.admin_or_course_related_prof
def course_students(request, course_id):
    if course_id is not None:
        course = get_object_or_404(M.Course, id=int(course_id))
    else:
        course = None
    if request.method == "POST":
        form = F.StudentToCourse(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            course.save()

        return HttpResponseRedirect(reverse('elearning:manageCourse', kwargs={'course_id': course_id}))

    else:
        form = F.StudentToCourse(instance=course)

    return render(request, 'courseStudentList.html', {'form': form,'course':course})


@login_required
@D.admin_only
def programme_modify(request, programme_id=None):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
    else:
        programme = None
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
        return HttpResponseRedirect(reverse('elearning:listProgrammes'))
    else:
        form = F.ProgrammeForm(instance=programme)
    return render(request, 'programmeEdit.html', {'form': form })


@login_required
@D.admin_only
def programme_manage(request, programme_id=None):
    programme = get_object_or_404(M.Programme, id=int(programme_id))
    if request.method == "POST":
        courseList = loads(request.POST['courseList'])
        courses = M.Course.objects.filter(programmes__id=programme.id)
        if courses:
            for course in courses:
                course.programmes.remove(programme)
        for courseID in courseList:
            course = get_object_or_404(M.Course, id=int(courseID))
            course.programmes.add(programme)
        return HttpResponse("Success")
    
    courses = M.Course.objects.all()
    for course in courses:
        if course.programmes.filter(id=programme.id).exists():
            course.checked = True
        else:
            course.checked = False
    
    return render(request, 'programmeMng.html', {'courses': courses, "programme" : programme })
                            
def programmes_show(request, programme_id=None):
    user = get_object_or_404(M.CustomUser, id=request.user.id)
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
        courses_in_programme = M.Course.objects.filter(programmes=programme)
        courses_elected = M.Course.objects.exclude(programmes=programme).filter(users=user)
        return render(request, 'courses.html', {'courses_in_programme': courses_in_programme, 'courses_elected': courses_elected, 'programme_id': programme_id})
    else:        
        programmes_inscribed = M.Programme.objects.filter(users=user)
        programmes_uninscribed = M.Programme.objects.exclude(users=user)
        return render(request, 'programmes.html', {'programmes_inscribed': programmes_inscribed, 'programmes_uninscribed': programmes_uninscribed })
    

@login_required
@D.admin_only
def programme_students(request, programme_id):
    if programme_id is not None:
        programme = get_object_or_404(M.Programme, id=int(programme_id))
    else:
        programme = None
    if request.method == "POST":
        form = F.StudentToProgramme(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            students = request.POST.getlist('users')
    
            for course in M.Course.objects.filter(programmes=programme):
                for student in students:
                    a = M.Course.objects.filter(id=course.id).filter(users=student)
                    if len(a)==0:
                        course.users.add(student)
            
        return HttpResponseRedirect(reverse('elearning:showProgramme', kwargs={'programme_id': programme_id}))
    else:
        form = F.StudentToProgramme(instance=programme)

    return render(request, 'programmeStudentList.html', {'form': form,'programme':programme})



@login_required
@D.admin_or_course_related_prof
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

@login_required
def add_student_to_programme(request, programme_id=None):
    programme = get_object_or_404(M.Programme, id=int(programme_id))
    user = get_object_or_404(M.CustomUser, id=request.user.id)
    if request.method == 'POST':
        for course in M.Course.objects.filter(programmes=programme):
                    a = M.Course.objects.filter(id=course.id).filter(users=user)
                    if len(a)==0:
                        course.users.add(user)
        programme.users.add(user)
        
    return HttpResponseRedirect(reverse('elearning:listProgrammes'))
            

@login_required
@D.admin_or_course_related_prof
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


@login_required
@D.admin_or_course_related_prof
def section_reorder_blocks(request, section_id):
    new_order = loads(request.POST['neworder'])
    for i in range(len(new_order)):
        block = get_object_or_404(M.Block, id=int(new_order[i]), sections=int(section_id))
        block.index = i
        block.save()
    return HttpResponse('')


@login_required
@D.admin_or_course_related_prof
def section_list_blocks(request, section_id):
    section = get_object_or_404(M.Section, id=int(section_id))
    query_results = M.Block.objects.filter(sections__id=section_id)
    response = serialize("json", query_results.order_by("index"))
    print response
    return HttpResponse(response)


@login_required
@D.admin_or_course_related_prof
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

def block_quiz(request, course_id, section_id, block_id):
    quizBlock = get_object_or_404(M.QuizBlock, id=int(block_id))
    try:
        progress = M.Progress.objects.filter(user=request.user).filter(block=quizBlock.id)
    except M.Block.DoesNotExist:
        progress = None
    if progress:
        if quizBlock.assessment:
            return HttpResponseForbidden()
        else:
            progress.delete()
    if request.method == "POST":
        form = F.ProgressForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse("Success!")
    else:
        initialDict = {
            'user': request.user.id,
            'block': quizBlock.id
        }
        form = F.ProgressForm(initial=initialDict)
        
    return render(request, 'quizShow.html', {"form": form, 'course_id': course_id,
                                              'section_id': section_id, 'block_id': block_id,
                                              'serial_questions' : quizBlock.serialQuestions })

def blocks_studentview(request, course_id, section_id):
    course = get_object_or_404(M.Course, id=int(course_id))
    section = get_object_or_404(M.Section, id=int(section_id))
    blocks = M.Block.objects.filter(sections__id=section_id).select_subclasses()
    
    for block in blocks:
        block.type = type(block).__name__
        if block.type == "QuizBlock":
            try:
                answers = M.Progress.objects.filter(user=request.user).filter(block=block.id)
            except M.Block.DoesNotExist:
                pass
            if answers:
                result = answers[0].assess()
                block.answers = result["result"]
                block.score = result["score"]
            else:
                block.answers = None
                block.score = None
    return render(request, 'sectionShow.html', {"course_id": course_id,
                                            "section": section,
                                            "blocks": blocks,
                                            "course":course})
