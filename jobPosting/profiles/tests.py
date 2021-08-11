from django.test import TestCase, Client
from jobPosting.profiles.models import Profile


class ProfileTestCase(TestCase):
    """
    Testing the profile functionality
    """

    def setUp(self) -> None:
        email = 'test@abv.bg'
        pwd = 'Qwerty1234!'

        self.profile_endpoint = '/profile/'

        self.c = Client()
        self.c.post('/auth/sign-up/', {'email': email, 'password1': pwd, 'password2': pwd})
        self.c.post('/auth/sign-in/', {'email': email, 'password': pwd})

    def test_profile_created(self):
        profile = Profile.objects.first()
        self.assertIsNotNone(
            profile, 'Profile was not created'
        )
        self.assertFalse(
            profile.is_complete, 'The profile was not created correctly'
        )

    def test_profile_get(self):
        response = self.c.get(self.profile_endpoint)
        self.assertEqual(response.status_code, 200, 'Incorrect status code')
        self.assertContains(response, 'Edit profile', msg_prefix='The edit profile view is not being displayed.')

    def test_profile_update(self):
        new_data = {
            'first_name': 'test',
            'last_name': 'user',
            'age': 20
        }
        self.c.post(self.profile_endpoint, new_data)
        profile = Profile.objects.first()
        self.assertEqual(profile.first_name, new_data['first_name'], 'The first name was not updated')
        self.assertEqual(profile.last_name, new_data['last_name'], 'The last name was not updated')
        self.assertEqual(profile.age, new_data['age'], 'The age was not updated')

        self.assertTrue(profile.is_complete)
