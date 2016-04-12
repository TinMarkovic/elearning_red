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

class ProgrammeForm(ModelForm):
    class Meta:
        model = M.Programme
        fields = ('name', 'desc','tags','avgRating')
    
class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())
 
