from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from users.models import Profile
from users.forms import UserRegistartionForm
import mock

class TestUsersRegisterView(TestCase):

    def test_register_method(self):

        data_registration = {
            'username': 'someuser',
            'email': 'aaa@company.com',
            'password1': 'tester123',
            'password2': 'tester123',
        }

        form = mock.Mock(return_value=True)
        
        if form.return_value:
            response = self.client.get(reverse('register'))
            request = self.client.post(f'/register/', data=data_registration)

            user = User.objects.get(username='someuser')

            resp_login = self.client.get(reverse('login'))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(request.status_code, 302)
            self.assertEqual(resp_login.status_code, 200)
            self.assertEqual(user.username, 'someuser')

            del user
    
    def test_user_profile(self):
        
        user = User.objects.create_user('Mark', email='mark@company.com', password='tester1234')
        profile = Profile.objects.create(user=user)

        login = self.client.login(username='Mark', password='tester1234')

        response = self.client.get(f'/profile/')
        request = self.client.post(f'/profile/', {'username':'Mark', 'email':'mark@company.com'})

        # print(response.content)
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(request.status_code, 302)
        self.assertIn(b'Mark', response.content)

        del user
        del profile
