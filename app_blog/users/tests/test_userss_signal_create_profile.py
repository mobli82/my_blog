from django.contrib.auth.models import User
from django.test import TestCase
from django.db.models import signals

from users.models import Profile
import mock

class TestSaveProfile(TestCase):

    @mock.patch('users.signals.create_profile')
    def test_should_send_signal_to_create_profile(self, create_profile):
        signals.post_save.disconnect(sender=User)

        create_profile.created = True
                
        if create_profile.created:
            Profile.objects.create(user=User.objects.create_user('Some user'))

        self.assertTrue(create_profile.called)

        # from django.db.models import signals
        # from users.signals import create_profile

        # reg_func = [func[1]() for func in signals.post_save.receivers]
        # self.assertIn(create_profile, reg_func)
        