from django.forms import ModelForm, widgets, ChoiceField, Form, CharField, PasswordInput, MultipleChoiceField
import models as M
from datetime import datetime

class UserForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'dob','role')
   	widgets = {
            'dob': widgets.SelectDateWidget(years=range((datetime.now().year-90),(datetime.now().year-15))), 'password': PasswordInput()
        }

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
    # Testna forma - bit ce prebrisana
    class Meta:
        model = M.HTMLBlock
        fields = ('name', 'index', 'sections', 'assessment', 'content')
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class VideoBlockForm(ModelForm):
    # TODO: Implement
    pass
    
class ImageBlockForm(ModelForm):
    # TODO: Implement
    pass
    
class QuizBlockForm(ModelForm):
    # TODO: Implement
    pass

class ProgrammeForm(ModelForm):
    class Meta:
        model = M.Programme
        fields = ('name', 'desc','tags','avgRating')
    
class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())

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
       
class ImageForm(ModelForm):
    class Meta:
        model = M.ImageBlock
        fields = ('name', 'title', 'sections', 'assessment', 'image')

class VideoForm(ModelForm):
    class Meta:
        model = M.VideoBlock
        fields = ('name', 'url', 'assessment')    
