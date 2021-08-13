from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy


class AuthTestCase(TestCase):
    """
    Testing the sign-up and sign-in functionalities
    """

    def setUp(self) -> None:
        self.UserModel = get_user_model()
        self.c = Client()
        self.email = 'test@abv.bg'
        self.pwd = 'Qwerty1234!'

    def test_register(self):
        login_data = {'email': self.email, 'password1': self.pwd, 'password2': self.pwd}
        self.c.post(reverse_lazy('sign up'), login_data)
        self.assertTrue(self.UserModel.objects.filter(email=self.email).exists())

    def test_register_short_pwd(self):
        email = 'test_fail@abv.bg'
        pwd = 'q!'
        login_data = {'email': email, 'password1': pwd, 'password2': pwd}
        self.c.post(reverse_lazy('sign up'), login_data)
        self.assertFalse(self.UserModel.objects.filter(email=self.email).exists())

    def test_login(self):
        response = self.c.post(reverse_lazy('sign in'), {'email': self.email, 'password': self.pwd})
        self.assertNotContains(response, 'Incorrect')
