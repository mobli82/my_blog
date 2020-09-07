from django.test import TestCase
from django.contrib.auth.models import User

from users.models import Profile
import mock

class TestUsersProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Cris')
        self.profile = Profile.objects.create(user=self.user)
        self.user.save()
        self.profile.save()
        self.user.refresh_from_db()

    def tearDown(self):
        del self.user
    
    def test_str_method(self):
        self.assertEqual(str(self.profile), 'Cris Profile')
    
    