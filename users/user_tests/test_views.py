from django.test import TestCase, Client
from django.urls import reverse

from users.models import CustomUser, Person
from django.utils import timezone

from datetime import datetime, timedelta

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.home_url = reverse('home')
        self.profile_url = reverse('prof')

        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.register_url = reverse('register')
        
        self.forgot_password_generator_url = reverse('forgot_pw')
        self.forgot_password_token_url = reverse('forgot_pw_token')
        self.forgot_password_new_url = reverse('forgot_pw_nw')
        self.activate_email_url = reverse('activate', kwargs={'uidb64': 1, 'token': 'token'})

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
        
        self.client.login(
            username = 'Test1',
            password = 'passwd'
        )

    def test_homepage_GET(self):
        response = self.client.get(self.home_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_profile_GET(self):
        response = self.client.get(self.profile_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_POST_change_person_data(self):
        response = self.client.post(self.profile_url, {
            'name': 'NewName',
            'surname': 'NewSurname',
            'age': 21,
            'github_url': 'https://github.com/new-test-account',
        }, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

        person = Person.objects.get(pk=1)

        self.assertEquals(person.name, 'NewName')
        self.assertEquals(person.surname, 'NewSurname')
        self.assertEquals(person.age, 21)
        self.assertEquals(person.github_url, 'https://github.com/new-test-account')

        messages = list(response.context['messages'])
        self.assertEquals(len(messages), 2)
        
        self.assertEquals(messages[0].message, "GitHub hesap bilgisi değiştirildiği için önceki postlar silindi")
        self.assertEquals(messages[0].tags, "warning")

        self.assertEquals(messages[1].message, "Profile bilgileri başarıyla değiştirildi")
        self.assertEquals(messages[1].tags, "success")
    
    def test_profile_POST_not_changed_github_url(self):
        response = self.client.post(self.profile_url, {
            'name': 'NewName',
            'surname': 'NewSurname',
            'age': 21,
            'github_url': 'https://github.com/test-account',
        }, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

        messages = list(response.context['messages'])
        self.assertEquals(len(messages), 1)
        
        self.assertEquals(messages[0].message, "Profile bilgileri başarıyla değiştirildi")
        self.assertEquals(messages[0].tags, "success")
    
    def test_login_GET(self):
        response = self.client.get(self.login_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_POST(self):
        
        self.user1.is_email_valid = True
        self.user1.save()
        
        response = self.client.post(self.login_url, {
            'username': 'Test1',
            'password': 'passwd',
        }, follow=True)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('home.html')

    def test_logout_GET(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('home.html')

    def test_register_GET(self):
        response = self.client.get(self.register_url, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed('users/register.html')

    # register post test not allowed because of email sender

    # activate user also related with email

    # email related sections not completed (BECAUSE I DON'T KNOW HOW TO CHECK!!!)
    
    # Email mocking will be used to imitate virtual environment of verification email
