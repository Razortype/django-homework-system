from django.test import TestCase, Client
from django.urls import reverse
from posts.models import Category, Homework, Post
from users.models import CustomUser, Person

from django.utils import timezone

from datetime import datetime, timedelta
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.homework_list_url = reverse('hw_list')
        self.homework_list_by_category_url = reverse('hw_list_by_category', args=['fake-category'])
        self.homework_detail_url = reverse('hw_detail_by_id', args=[1])

        self.post_new_url = reverse('post_new', kwargs={'_id':1})
        self.post_update_url = reverse('post_update', kwargs={'homework_id':1,'post_id':1})
        self.post_delete_url = reverse('post_delete', kwargs={'homework_id':1,'post_id':1})

        self.category1 = Category.objects.create(
            name="Category - Test",
            color="000000",
            description="test description test descrption",
        )

        self.homework1 = Homework.objects.create(
            name="Homework - Test",
            category=self.category1,
            description="test description test descrption",
            expired_date=timezone.now()   
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

        self.client.login(username="Test1" ,password="passwd")

    def test_homework_list_GET(self):        
        response = self.client.get(self.homework_list_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/homework_list.html')

    def test_homework_list_by_category_GET(self):
        response = self.client.get(self.homework_list_by_category_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/homework_list.html')

    def test_homework_detail_GET(self):
        response = self.client.get(self.homework_detail_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/homework_detail.html')

    def test_homework_detail_POST_add_new_post(self):

        response = self.client.post(self.post_new_url, {
            'github_url': 'https://github.com/test-account/test-project',
        }, follow=True)

        self.assertEquals(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEquals(len(messages), 1)
        message = messages[0]
        
        self.assertEquals(message.message, "Post başarıyla atıldı")
        self.assertEquals(message.tags, "success")

    def test_homework_detail_POST_update_post(self):

        self.client.post(self.post_new_url, {
            'github_url': 'https://github.com/test-account/test-project',
        }, follow=True)

        response = self.client.post(self.post_update_url, {
            'github_url': 'https://github.com/test-account/test-project-2',
        }, follow=True)

        self.assertEquals(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEquals(len(messages), 1)
        message = messages[0]

        self.assertEquals(message.message, "Post başarıyla değiştirildi")
        self.assertEquals(message.tags, "success")

    def test_homework_detail_POST_delete_post(self):

        self.client.post(self.post_new_url, {
            'github_url': 'https://github.com/test-account/test-project',
        }, follow=True)

        response = self.client.get(self.post_delete_url, follow=True)

        self.assertEquals(response.status_code, 200)

        messages = list(response.context['messages'])
        self.assertEquals(len(messages), 1)
        message = messages[0]

        self.assertEquals(message.message, "Post başarıyla silindi")
        self.assertEquals(message.tags, "success")