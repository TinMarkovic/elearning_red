from datetime import date
from django.forms import ModelForm, widgets
from .models import CustomUser, Course

class UserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'dob')
        
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'desc', 'beginDate', 'duration', 'author', 'tags')
        widgets = {
            'beginDate': widgets.SelectDateWidget(),
        }