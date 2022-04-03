from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from articles.models import User
import structlog

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form_field in self.fields.values():
            form_field.widget.attrs['class'] = 'form-control'
            form_field.widget.attrs['placeholder'] = form_field.label

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if len(username) == 0:
    #         self.add_error('required', 'ユーザー名を入力してください')
    #         raise forms.ValidationError
    #     registerd_users = User.objects.all()
    #     if username in registerd_users:
    #         raise ValueError('このユーザー名は既に使われています')
    #     return username

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['class'] = 'form-control'
       self.fields['username'].widget.attrs['placeholder'] = 'User name'
       self.fields['password'].widget.attrs['placeholder'] = 'Password'

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     if len(username) == 0:
    #         self.add_error('required', 'ユーザー名を入力してください')
    #         raise forms.ValidationError
    #     return username
        

# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = Article
#         fields = '__all__'
        

    # Choices = (('good_eval', 'いいね'), ('uninterested_eval', '興味なし'))
    # user_choices = forms.fields.ChoiceField(
        # choices=Choices,
        # widget=forms.RadioSelect )
    # user_choices.widget.attrs.update({'required':False, 'checked':False})
    
    # def get_bound_data(self):
    #     logger = structlog.get_logger(__name__)
    #     logger.info('get_bound_data()')
    #     logger.error(self.user_choices.widget.attrs['checked'])

    # def __init__(self, *args, **keyargs):
    #     super(ChoiceForm, self).__init__(*args, **keyargs)
    #     Choices = (('choice0', 'test_0'), ('choice1', 'test_1'))
    #     self.user_choices = forms.fields.ChoiceField(
    #         choices=Choices,
    #         widget=forms.RadioSelect )
    #     self.user_choices.widget.attrs.update({'checked':True})