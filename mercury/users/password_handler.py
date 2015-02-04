import django
import os, sys

#django.setup()
sys.path.append(os.path.join(os.path.dirname(__file__), 'around'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'around.settings'
from django.conf import settings
settings.configure()

import django.contrib.auth.hashers as Hasher

class PasswordHandler:
    def __init__(self, pw_plain_text, pw_hashed=None):
        self.password_plain = pw_plain_text
        self.password_hashed = pw_hashed
        self.hasher = Hasher

    def authenticate(self):
        if self.hasher.check_password(self.password_plain, self.password_hashed):
            print 'passwords match'
            return True
        print 'passwords do not match'
        return False

    def hash(self):
        return self.hasher.make_password(self.password_plain).encode()

    def remove_leading_and_trailing_whitespaces(self):
        back = len(self.password_plain)-1
        front = 0
        cont_front = True
        cont_back = False
        print 'password before white spaces %s', self.password_plain
        for i in range(len(self.password_plain)):
            front = i
            leading = self.password_plain[i]
            following = self.password_plain[back]
            if leading != ' ':
                cont_front = False
            if following != ' ':
                cont_back = False
            if cont_back:
                back -= 1
            if i == back or not cont_back or not cont_front:
                break
        if front == back:
            return ''
        cleaned_pw = self.password_plain[front:back+1]
        print 'password after cleaning: %s' % cleaned_pw
        return cleaned_pw
