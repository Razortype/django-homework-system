from django.test import TestCase

from posts.forms import HomeworkForm, HomeworkDetailForm, PostForm
from posts.models import Category, Homework

from django.utils import timezone

class TestForms(TestCase):

    def setUp(self):
        
        self.category_1 = Category.objects.create(
            name="Category - Test",
            color="000000",
            description="test description test descrption",
        )

        self.homework1 = Homework.objects.create(
            name="Homework - Test",
            category=self.category_1,
            description="test description test descrption",
            expired_date=timezone.now()   
        )

    def test_homework_form_valid_data(self):
        form = HomeworkForm(data={
            'name': "Test homework name",
            'category': self.category_1.pk,
            'start_at': timezone.now(),
            'expired_date': timezone.now(),
        })

        self.assertTrue(form.is_valid())

    def test_homework_form_no_data(self):
        form = HomeworkForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_homework_detail_form_valid_data(self):
        form = HomeworkDetailForm(data={
            'homework':self.homework1.pk,
            'detail_name': 'Test Detail',
            'detail_risk':'H',
        })

        self.assertTrue(form.is_valid())

    def test_homework_detail_form_no_data(self):
        form = HomeworkDetailForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_post_form_valid_data(self):
        form = PostForm(data={
            'github_url':'https://www.github.com/test-account',
        })

        self.assertTrue(form.is_valid())

    def test_post_form_no_data(self):
        form = PostForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)