from django.test import TestCase

from users.utils import generate_token, valid_checker, generate_6_digit_number, generate_forgot_token
from users.models import CustomUser, Person, UserToken

from django.utils import timezone

from datetime import datetime, timedelta

class TestUtils(TestCase):

    def setUp(self):

        CustomUser.objects.create_user(
            email    = "test1@example.com",
            username = "Test1",
            password = "passwd1",
        )
        self.user1 = CustomUser.objects.get(pk=1)

        CustomUser.objects.create_user(
            email    = "test2@example.com",
            username = "Test2",
            password = "passwd2",
        )
        self.user2 = CustomUser.objects.get(pk=2)

        self.person1 = Person.objects.create(
            user       = self.user1,
            name       = "testname1",
            surname    = "testsurname1",
            age        = 18,
            github_url = "https://github.com/test1-account-1"
        )
        
        self.person2 = Person.objects.create(
            user       = self.user2,
            name       = "testname2",
            surname    = "testsurname2",
            age        = 19,
            github_url = "https://github.com/test1-account-2"
        )

    def test_generate_hash_token_function(self):
        token = generate_token.make_token(self.user1)
        head, tail = token.split('-')

        self.assertEquals(head[0], "b")
        self.assertEquals(len(head), 6)
        self.assertEquals(len(tail), 32)

    # def test_check_hash_token_function(self):
    #     raise NotImplementedError('Hash checking function is not implemented')

    def test_check_password_valid_function_VALID(self):
        password1 = "Password123."
        password2 = "Password123."
        
        errors = valid_checker.check_password_valid(password1, password2)

        self.assertEquals(len(errors), 0)

    def test_check_password_valid_function_INVALID(self):
        password1 = "@@@@"
        password2 = "@@@@@"

        errors = valid_checker.check_password_valid(password1, password2)

        self.assertEquals(len(errors), 6)

    def test_check_account_valid_function_VALID(self):
        username = "Test3"
        email    = "test3@example.com"
        github_url = "https://github.com/test1-account-3"

        errors = valid_checker.check_account_valid(username, email, github_url)
        self.assertEquals(len(errors), 0)

    def test_check_account_valid_function_INVALID_not_github_url(self):
        username = "Test3"
        email    = "test3@example.com"
        github_url = "https://google.com"

        errors = valid_checker.check_account_valid(username, email, github_url)
        self.assertEquals(len(errors), 1)
        self.assertEquals(errors[0], "Github URL geçerli bir hesap değildir")

    def test_check_account_valid_function_INVALID_already_in_use(self):
        username   = self.user1.username
        email      = self.user1.email
        github_url = self.person1.github_url

        errors = valid_checker.check_account_valid(username, email, github_url)
        self.assertEquals(len(errors), 3)
        self.assertNotIn('Github URL geçerli bir hesap değildir', errors)

    def test_generate_6_digit_number_function(self):
        generated_token = generate_6_digit_number()

        self.assertEquals(len(generated_token), 6)
        self.assertTrue(generated_token.strip().isdigit(), msg="Given value is not numeric")

    def test_generate_forgot_token_function(self):
        generated_token = generate_forgot_token()
        self.assertEquals(UserToken.objects.filter(token=generated_token).count(), 0)