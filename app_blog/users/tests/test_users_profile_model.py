from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings

from users.models import Profile
import mock
from PIL import Image
import os

class TestUsersProfileModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('Jack')
        self.profile = Profile.objects.create(user=self.user)
        # self.user.save()
        # self.profile.save()
        # self.user.refresh_from_db()

    def tearDown(self):
        del self.user
        del self.profile
    
    def test_str_method(self):
        self.assertEqual(str(self.profile), 'Jack Profile')
    
    def test_check_user_profile_size(self):
        usr = User.objects.create_user('Nick')
        profile = Profile.objects.create(user=usr)
        
        image = mock.MagicMock()
        image.path = profile.profile_img.path
        image.width = 200
        image.height = 200

        # print(dir(image))

        if image.width > 120 and image.height > 120:
            image.width = 80
            image.height = 80

        self.assertEqual(image.width, 80)
        self.assertEqual(image.height, 80)

        del usr
        del profile
    

    def test_url_img_path(self):
        self.assertTrue(os.path.exists(self.profile.profile_img.path))