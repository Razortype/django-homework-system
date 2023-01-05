from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import CustomUser, UserToken

from random import randint
import six
import threading
import re

class TokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user: CustomUser, timestamp: int) -> str:
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_valid)


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def check_password_valid(password1, password2):

        tests = {
            'Şifre ve şifre tekrarı eşleşmeli': password1 != password2,
            'Şifre uzunluğu 8 karakterden uzun olmalıdır': len(password1) < 8,
            'Bütün karakterler rakam olamaz': re.search(r"\d", password1) is None,
            'Şifre en az bir tane büyük harf içermelidir': re.search(r"[A-Z]", password1) is None,
            'Şifre en az bir tane küçük harf içermelidir': re.search(r"[a-z]", password1) is None,
            'Şifre en az bir tane sembol içermelidir': re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password1) is None,
        }
        
        return [name for name,res in tests.items() if res]

def generate_6_digit_number():
    range_start = 10**5
    range_end = (10**6)-1
    token = randint(range_start, range_end)
    return str(token)

def generate_forgot_token():
    generated_token = generate_6_digit_number()
    if UserToken.objects.filter(token=generated_token).exists():
        return generate_forgot_token()
    return generated_token

# Variables
generate_token = TokenGenerator()