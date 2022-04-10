from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from articles.models import User

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form_field in self.fields.values():
            form_field.widget.attrs['class'] = 'form-control'
            form_field.widget.attrs['placeholder'] = form_field.label

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'
       self.fields['username'].widget.attrs['placeholder'] = 'User name'
       self.fields['password'].widget.attrs['placeholder'] = 'Password'
