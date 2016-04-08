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

""" 
class CreateStudentForm(forms.ModelForm):
    class Meta(object):
        model = Student
        fields = ('first_name', 'last_name', 'age', 'about')

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age > 100:
            raise forms.ValidationError("Too old student")
        return age

    def clean(self):
        cleaned_data = super(CreateStudentForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if first_name and last_name and first_name == last_name:
            raise forms.ValidationError("First and last names cannot be the same!")
        return cleaned_data
"""