from django.test import TestCase
from users.models import CustomUser, Person

from django.utils import timezone

from datetime import datetime, timedelta
import mock

class TestModel(TestCase):
    
    def setUp(self):

        CustomUser.objects.create_user(
            email="text@example.com",
            username="Test1",
            password="passwd",
        )
        self.user1 = CustomUser.objects.get(pk=1)

        self.person1 = Person.objects.create(
            user=self.user1,
            name="test1",
            surname="test2",
            age=21,
            github_url="https://github.com/test-account",
        )

    def test_person_is_assigned_on_creation(self):
        self.assertEquals(self.person1.user, self.user1)

    def test_user_verification_token_expired_EXPIRED(self):
        # Mock time is not working
        pass

    def test_user_verification_token_expired_NOT_EXPIRED(self):
        # Mock time is not working
        pass

    def test_user_forgot_token_expired_EXPIRED(self):
        # Mock time is not working
        pass

    def test_user_forgot_token_expired_NOT_EXPIRED(self):
        # Mock time is not working
        pass