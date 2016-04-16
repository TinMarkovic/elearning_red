from django.forms import ModelForm, widgets, Form, CharField, Textarea, IntegerField
import models as M

class UserForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'dob')
        widgets = {
            'dob': widgets.SelectDateWidget(),
        }
        
class CourseForm(ModelForm):
    class Meta:
        model = M.Course
        fields = ('name', 'desc', 'beginDate', 'duration', 'author', 'tags')
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
        
class HTMLBlockForm(ModelForm):
    class Meta:
        model = M.HTMLBlock
        fields = ('name', 'index', 'sections', 'assessment', 'content')
        widgets = {
            'sections': widgets.HiddenInput(),
            'index': widgets.HiddenInput(),
        }
    
class VideoBlockForm(ModelForm):
    pass
    
class ImageBlockForm(ModelForm):
    pass
    
class QuizBlockForm(ModelForm):
    pass

class LoginForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'password')
