from django.forms import ModelForm, widgets, ChoiceField, Form, CharField, PasswordInput, MultipleChoiceField, Select, IntegerField, ModelMultipleChoiceField, DateField
import models as M
from datetime import datetime
from suit_ckeditor.widgets import CKEditorWidget
from registration.forms import RegistrationForm

class UserForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'dob','role')
        widgets = {
            'dob': widgets.SelectDateWidget(years=range((datetime.now().year-90),(datetime.now().year-15))), 'password': PasswordInput()
        }
        
class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())        

class CourseForm(ModelForm):
    class Meta:
        model = M.Course
        fields = ('name', 'desc', 'beginDate', 'duration', 'author', 'programmes', 'tags')
        widgets = {
            'beginDate': widgets.SelectDateWidget()
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
        
class HTMLBlockForm(ModelForm):
    class Meta:
    	model = M.HTMLBlock
    	fields = ('name', 'index', 'sections', 'assessment', 'content',) 
    	widgets = {
                'content': CKEditorWidget(),
                'sections': widgets.HiddenInput(),
                'index': widgets.HiddenInput(),
            }
               
class VideoBlockForm(ModelForm):
    class Meta:
        model = M.VideoBlock
        fields = ('name', 'index', 'sections', 'url', 'assessment') 
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class ImageBlockForm(ModelForm):
    class Meta:
        model = M.ImageBlock
        fields = ('name', 'subtitle', 'index', 'sections', 'assessment', 'image')
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class QuizBlockForm(ModelForm):
    # TODO: Implement
    pass

class ProgrammeForm(ModelForm):
    courses = ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = M.Programme
        fields = ('name', 'desc','tags','avgRating')
	
    def __init__(self, *args, **kwargs):
	super(ProgrammeForm, self).__init__(*args, **kwargs)
	self.fields['courses'].queryset = M.Course.objects.all()

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
