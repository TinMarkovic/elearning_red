

from django.shortcuts import render, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.utils.translation import ugettext
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages


from forms import UserForm, CourseForm, ImageForm, VideoForm, StudentToCourse
from .models import CustomUser, Course
from .models import Role, ImageBlock, VideoBlock

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
"""
def user_login(request):
    if request.method == "POST":
        username= request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password=password)

        return HttpResponseRedirect('')
    else:
        form = LoginForm()   

    return render(request, 'index.html', {'form': form}) """


#@permission_required('elearning.can_edit', raise_exception=True)
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
    return None; 

def homepage(request):    
    message = ugettext('Welcome to ElearningRed!')
    return render(request, 'base.html', {'message': message})

#decorator da mogu samo profesori i admin pristupit
#@login_required
#@permission_required('elearning.can_add', raise_exception=True)


#ne dirat
def students (request, course_id):
    if course_id is not None:
        course = get_object_or_404(Course, id=int(course_id))
    else:
        course = None
        
    query_results = CustomUser.objects.filter(role__name__exact="Student")     
    if request.method == "POST":
        form = StudentToCourse(request.POST, instance=course)
        
        if form.is_valid():
            course = form.save()
            # TODO: Add the validated professor to the users - for editing
            course.save()
        
        return HttpResponseRedirect('') 
        
    else: 
        form = StudentToCourse(instance=course)
        
    return render(request, 'addstudents.html', {'form': form, 'query_results': query_results})

#course_details
def detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
        coursedet =Course.objects.all()
        
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render( request, 'detail.html', {"course" : course, "coursedet" : coursedet})

#za imagecreate
def post_list (request):
   
    files = ImageBlock.objects.all()

    return render(request, 'list.html',{'files':files, })
   



#testno za blokove
#kreiranje
def post_create(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    # i = ImageBlock(image=request.FILES['image'])
    if form.is_valid():
        #validate professors
            instance = form.save()
        #instance.user = request.user
            instance.save()
        #form.save()
            messages.success(request, "Uspilo")
            return HttpResponseRedirect('list')
#else: 
    #form = ImageForm(instance=iblock) 
    #messages.error(request, "Nije")
    return render(request, 'image_create.html', {'form': form}) 




#def post_delete(request):

def post_show(request, id=None):
    if id is not None:
        image = get_object_or_404(ImageBlock, id=id)
        print image
        print image.image

        return render(request, 'image_show.html',{'image' : image})
    else:
        query_results = ImageBlock.objects.all()
        return render(request, 'image_show.html', {"query_results" : query_results})   



def video_create(request, video_id=None):
    if video_id is not None:
        video = get_object_or_404(Course, id=int(video_id))
    else:
        video = None
    if request.method == "POST":
        form = VideoForm(request.POST, instance=video)
        
        if form.is_valid():
            # TODO: Add the validated professor to the users - for editing
            form.save()
        
        return HttpResponseRedirect('video_list') 
        
    else: 
        form = VideoForm(instance=video) 
        
    return render(request, 'video_add.html', {'form': form}) 

def video_list (request):
   
    files = VideoBlock.objects.all()

    return render(request, 'video_list.html',{'files':files, })

