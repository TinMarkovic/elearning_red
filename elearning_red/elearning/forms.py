from django.forms import ModelForm, widgets, ChoiceField, Form, CharField, PasswordInput, MultipleChoiceField, Select, IntegerField, ModelMultipleChoiceField, DateField, ModelChoiceField
from django.shortcuts import render
import models as M
from datetime import datetime
from suit_ckeditor.widgets import CKEditorWidget
from registration.forms import RegistrationForm

class UserForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'dob','role')
        widgets = {
            'dob': widgets.SelectDateWidget(years=range((datetime.now().year-90),(datetime.now().year-15))),
        }
        
class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())        

class CourseForm(ModelForm):
    class Meta:
        model = M.Course
        fields = ('name', 'desc', 'beginDate', 'duration', 'author', 'programmes', 'tags')
        widgets = {
            'beginDate': widgets.SelectDateWidget(),
        }

class SectionForm(ModelForm):
    class Meta:
        model = M.Section
        fields = ('name', 'desc', 'beginDate', 'index', 'course', )
        widgets = {
            'beginDate': widgets.SelectDateWidget(),
            'course': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
        
class BlockForm(ModelForm):
    def getRender(self, request, course_id = None, section_id = None):
        return render(request, 'blockEdit.html', {'form': self})

class HTMLBlockForm(BlockForm):
    class Meta:
    	model = M.HTMLBlock
    	fields = ('name', 'index', 'sections', 'content',) 
    	widgets = {
            'content': CKEditorWidget(),
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
               
class VideoBlockForm(BlockForm):
    class Meta:
        model = M.VideoBlock
        fields = ('name', 'index', 'sections', 'url',) 
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class ImageBlockForm(BlockForm):
    class Meta:
        model = M.ImageBlock
        fields = ('name', 'subtitle', 'index', 'sections', 'image')
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class QuizBlockForm(BlockForm):
    class Meta:
        model = M.QuizBlock
        fields = ('name', 'index', 'sections', 'assessment', 'serialQuestions')
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
            'serialQuestions': widgets.HiddenInput(),
        }
    def getRender(self, request, course_id = None, section_id = None):
        return render(request, 'quizEdit.html', {'form': self, "course_id": course_id, "section_id": section_id, })

class ProgressForm(BlockForm):
    class Meta:
        model = M.Progress
        fields = ('user', 'block', 'serialAnswers')
        widgets = {
            'user': widgets.HiddenInput(),
            'block': widgets.HiddenInput(),
            'serialAnswers': widgets.HiddenInput(),
        }


class ProgrammeForm(ModelForm):
    class Meta:
        model = M.Programme
        fields = ('name', 'desc','tags','avgRating','users',)
        widgets = {
            'users': widgets.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super(ProgrammeForm, self).__init__(*args, **kwargs)                
        self.fields['users'].queryset = self.fields['users'].queryset.filter(role__name__exact="Student")

class RatingForm(ModelForm):
    class Meta:
	model = M.Rating
	fields = ('value',)

class StudentToCourse(ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentToCourse, self).__init__(*args, **kwargs)
        self.fields['users'].queryset = self.fields['users'].queryset.filter(role__name__exact="Student")    
    class Meta:
        model = M.Course       
        fields = ( 'users',)
        widgets = {
            'users': widgets.CheckboxSelectMultiple(),
        }

class CustomRegistrationForm(RegistrationForm):
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    dob = DateField(widget=widgets.SelectDateWidget(years=range((datetime.now().year-90),(datetime.now().year-15))))

class CustomRegistrationFormAdmin(CustomRegistrationForm):
    role = ModelChoiceField(queryset=M.Role.objects.all().order_by('name'))
    