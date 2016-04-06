from django.forms import ModelForm
from .models import CustomUser

class UserForm(ModelForm):
    class Meta:
	model = CustomUser
	fields = ('username', 'first_name', 'last_name', 'email', 'password', 'dob')
