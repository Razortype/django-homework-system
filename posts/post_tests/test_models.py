from django.test import TestCase
from posts.models import Category, Homework, HomeworkDetail, Post
from users.models import CustomUser, Person

from django.utils import timezone

from datetime import datetime, timedelta
import mock

class TestModel(TestCase):

    def setUp(self):

        self.category_1 = Category.objects.create(
            name="Category - Test",
            color="000000",
            description="test description test descrption",
        )

        self.homework_1 = Homework.objects.create(
            name="Homework - expired - started",
            category=self.category_1,
            description="test description test descrption",
            start_at=timezone.now() - timedelta(days=10),
            expired_date=timezone.now() - timedelta(days=5),
        )

        self.homework_2 = Homework.objects.create(
            name="Homework - not expired - not started",
            category=self.category_1,
            description="test description test descrption",
            start_at=timezone.now() + timedelta(days=5),
            expired_date=timezone.now() + timedelta(days=10),
        )

        self.homework_detail_1 = HomeworkDetail.objects.create(
            homework=self.homework_1,
            detail_name="test detail",
            detail_description="test detail description test detail descrption",
            detail_risk="H",
        )

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

    def test_homework_category_is_assigned_on_creation(self):
        self.assertEquals(self.homework_1.category.name, self.category_1.name)

    def test_homewowk_is_check_started_STARTED(self):
        self.assertTrue(self.homework_1.check_started())

    def test_homework_is_check_started_NOT_STARTED(self):
        self.assertFalse(self.homework_2.check_started())

    def test_homework_is_check_expired_EXPIRED(self):
        self.assertTrue(self.homework_1.check_expired())

    def test_homework_is_check_expired_NOT_EXPIRED(self):
        self.assertFalse(self.homework_2.check_expired())

    def test_post_get_time_diff(self):
        # Mocking time now worked for auto_now field
        # Need check if returned different time value is non-negative value
        pass