from django.test import TestCase

from users.forms import LoginForm, SignUserForm, ForgotPasswordForm, TokenForm, PersonForm, EmailForm
# from users.models import 

from django.utils import timezone

class TestForms(TestCase):

    def setUp(self):
        pass

    def test_login_form_valid_data(self):
        form = LoginForm(data={
            'username': 'user',
            'password': 'passwd'
        })

        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())

    def test_sign_user_form_valid_data(self):
        form = SignUserForm(data={
            'username': 'test_user',
            'email': 'test@test-account.com',
            'password1': 'passwordtest',
            'password2': 'passwordtest',
        })

        self.assertTrue(form.is_valid())

    def test_sign_user_form_no_data(self):
        form = SignUserForm(data={})

        self.assertFalse(form.is_valid())

    def test_forgot_password_form_is_valid(self):
        form = ForgotPasswordForm(data={
            'password1': 'test-password',
            'password2': 'test-password',
        })

        self.assertTrue(form.is_valid())

    def test_forgot_password_form_no_data(self):
        form = ForgotPasswordForm(data={})

        self.assertFalse(form.is_valid())

    def test_token_form_valid_data(self):
        form = TokenForm(data={
            'token': '123456',
        })

        self.assertTrue(form.is_valid())

    def test_token_form_no_data(self):
        form = TokenForm(data={})

        self.assertFalse(form.is_valid())

    def test_email_form_valid_data(self):
        form = EmailForm(data={
            'email': 'test.account@test-account.com'
        })

        self.assertTrue(form.is_valid())

    def test_email_form_no_data(self):
        form = EmailForm(data={})

        self.assertFalse(form.is_valid())

    def test_person_form_valid_data(self):
        form = PersonForm(data={
            'name': 'Name',
            'surname': 'Surname',
            'age': '18',
            'github_url': 'https://www.github.com/user-account',
        })

        self.assertTrue(form.is_valid())

    def test_person_form_no_data(self):
        form = PersonForm(data={})

        self.assertFalse(form.is_valid())