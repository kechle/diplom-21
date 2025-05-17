from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from courses.models import Course

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'avatar']

class AddStudentToCourseForm(forms.Form):
    student = forms.ModelChoiceField(queryset=User.objects.filter(is_student=True))
    course = forms.ModelChoiceField(queryset=Course.objects.all()) 