from django.test import SimpleTestCase
from django.urls import reverse, resolve

from users import views

class TestUrls(SimpleTestCase):
    
    def test_url_home_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, views.Home)

    def test_url_profile_is_resolved(self):
        url = reverse('prof')
        self.assertEquals(resolve(url).func.view_class, views.Profile)

    def test_url_login_is_resoved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, views.LoginView)

    def test_url_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, views.LogoutView)

    def test_url_register_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func.view_class, views.Register)

    def test_url_forgot_password_generate_is_resolved(self):
        url = reverse('forgot_pw')
        self.assertEquals(resolve(url).func.view_class, views.ForgotPasswordGenerate)

    def test_url_forgot_password_token_is_resolved(self):
        url = reverse('forgot_pw_token')
        self.assertEquals(resolve(url).func.view_class, views.ForgotPasswordToken)

    def test_url_forgot_password_new_is_resolved(self):
        url = reverse('forgot_pw_nw')
        self.assertEquals(resolve(url).func.view_class, views.ForgotPassword)

    def test_url_activate_user_is_resolved(self):
        url = reverse('activate', kwargs={'uidb64': 1, 'token': 'token'})
        self.assertEquals(resolve(url).func.view_class, views.ActivateUser)