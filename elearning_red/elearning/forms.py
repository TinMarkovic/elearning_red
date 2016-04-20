from django.forms import ModelForm, widgets, ChoiceField, Form, CharField, PasswordInput, MultipleChoiceField, Select, IntegerField, ModelMultipleChoiceField
import models as M
from datetime import datetime
from suit_ckeditor.widgets import CKEditorWidget

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
    #courses = CharField(widget=Select(choices=[choice.name for choice in M.Course.objects.all()]))
    courses = ModelMultipleChoiceField(queryset=None)
    class Meta:
        model = M.Programme
        fields = ('name', 'desc','tags','avgRating')
	
    def __init__(self, *args, **kwargs):
	super(ProgrammeForm, self).__init__(*args, **kwargs)
	self.fields['courses'].queryset = M.Course.objects.all()

class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())

class HTMLBlockForm(ModelForm):
    class Meta:
	model = M.HTMLBlock
	fields = '__all__' 
	widgets = {
            'content': CKEditorWidget(editor_options={'startupFocus': True})
        }

class RatingForm(ModelForm):
    class Meta:
	model = M.Rating
	fields = ('value',)
	"""
	widgets = {
	    'value': ChoiceField(choices=[(1, 1), (2, 2)])
	}
	"""
