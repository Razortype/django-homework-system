from django.test import TestCase

from posts.utils import get_timestamp, seperate_homeworks, check_post_404
from posts.models import Category, Homework

from django.utils import timezone

from datetime import datetime, timedelta

class TestUtils(TestCase):

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

    def test_get_timestamp_function(self):
        dt = datetime(2021, 5, 12)
        self.assertEquals(get_timestamp(dt),1620777600.0)

    def test_seperate_homeworks_function(self):
        passed, failed = seperate_homeworks(Homework.objects.all())

        passed_homework = passed[0]
        failed_homework = failed[0]

        self.assertEquals(passed_homework.name, "Homework - not expired - not started")
        self.assertEquals(failed_homework.name, "Homework - expired - started")

    def test_left_started_homeworks_function(self):
        
        homeworks = [i for i in Homework.objects.all() if i.check_started()]
        self.assertEquals(len(homeworks), 1)
        
        homework = homeworks[0]
        self.assertEquals(homework.name, self.homework_1.name)

    def test_check_post_404_function_VALID(self):
        valid_github_url = "https://github.com/Razortype/Python-QA-Manager"
        res = check_post_404(valid_github_url)
        self.assertFalse(res)

    def test_check_post_404_function_ERROR(self):
        invalid_github_url = "https://github.com/test/test-project"
        res = check_post_404(invalid_github_url)
        self.assertTrue(res)