from django.contrib.auth import get_user_model
from django.test import TestCase, Client


class AuthTestCase(TestCase):
    """
    Testing the sign-up and sign-in functionalities
    """

    def setUp(self) -> None:
        self.UserModel = get_user_model()
        self.c = Client()
        self.email = 'test@abv.bg'
        self.pwd = 'Qwerty1234!'
        self.sign_up_endpoint = '/auth/sign-up/'
        self.sign_in_endpoint = '/auth/sign-in/'

    def test_register(self):
        login_data = {'email': self.email, 'password1': self.pwd, 'password2': self.pwd}
        self.c.post(self.sign_up_endpoint, login_data)
        user = self.UserModel.objects.filter(email=self.email)
        self.assertEqual(len(user), 1)

    def test_register_short_pwd(self):
        email = 'test_fail@abv.bg'
        pwd = 'q!'
        login_data = {'email': email, 'password1': pwd, 'password2': pwd}
        self.c.post(self.sign_up_endpoint, login_data)
        user = self.UserModel.objects.filter(email=email)
        self.assertEqual(len(user), 0)

    def test_login(self):
        response = self.c.post(self.sign_in_endpoint, {'email': self.email, 'password': self.pwd})
        self.assertNotContains(response, 'Incorrect')
