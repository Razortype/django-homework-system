from .models import CustomUser

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import threading

class TokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user: CustomUser, timestamp: int) -> str:
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_valid)


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


# Variables
generate_token = TokenGenerator()