from django.forms import ModelForm, widgets
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

class LoginForm(ModelForm):
    class Meta:
        model = M.CustomUser
        fields = ('username', 'password')        