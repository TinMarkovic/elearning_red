from django.forms import ModelForm, widgets, Form, forms, MultipleChoiceField
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
        fields = ('name', 'desc', 'beginDate', 'duration', 'author', 'tags', )
        widgets = {
            'beginDate': widgets.SelectDateWidget(),
        }

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