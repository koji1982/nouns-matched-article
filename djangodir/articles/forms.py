from django import forms
from articles.models import Article
import structlog

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