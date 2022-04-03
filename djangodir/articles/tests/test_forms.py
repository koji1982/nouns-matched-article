from django.test import TestCase
from articles.forms import *

class FormsTest(TestCase):
    pass
    # def test_clean_username_raise_error(self):
    #     username = 'test_user'
    #     # User.objects.create_user(username)
    #     data = { 'username': username, 'password1': 'test_password', 'password2': 'test_password'}
    #     form = SignupForm(data)
    #     form.save()
    #     user = User.objects.get(username=username)
    #     self.assertEqual(user.username, username)
    #     # data['username'] = 'test_user2'

    #     form = SignupForm(data)
    #     form.save()
    #     user2 = User.objects.get(username=data['username'])
    #     self.assertEqual(user2.username, 'test_user2')
    #     print('count' + str(User.objects.count()))
            
        