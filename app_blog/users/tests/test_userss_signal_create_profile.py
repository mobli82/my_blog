from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Profile
import mock

class TestSaveProfile(TestCase):

    def test_should_send_signal_to_create_profile(self):
        user = User.objects.create_user('New user', 'new_user@company.com')
        user.save()

        from django.db.models import signals
        from users.signals import create_profile

        reg_func = [func[1]() for func in signals.post_save.receivers]
        self.assertIn(create_profile, reg_func)
        