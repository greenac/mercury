from password_handler import PasswordHandler
from users.models import User
from response import Response
import datetime
from date_handler import DateHandler

import django
django.setup()

class UserHandler:
    def __init__(self, user_dict):
        self.user_dict = user_dict
        self.property_name = UserProperties()
        self.date_handler = DateHandler()
        self.response_number = -1

    def username(self):
        return self.user_dict['username']

    def password(self):
        return self.user_dict['password']

    def get_user(self):
        try:
            user = User.objects.filter(username=self.username())[0]
        except IndexError:
            user = None
            pass
        return user

    def user_as_dict(self):
        user = self.get_user()
        if user:
            self.response_number = Response().USERNAME_AND_PASSWORD_CORRECT
            return user.as_dict()
        self.response_number = Response().USER_DOES_NOT_EXIST
        return {}

    def authenticate(self, user):
        pw_handler = PasswordHandler(pw_plain_text=self.password())
        responses = Response()
        if user.password == pw_handler.hash():
            # user exists and password matches password in database
            did_authenticate = True
            self.response_number = responses.USERNAME_AND_PASSWORD_CORRECT
        else:
            did_authenticate = False
            self.response_number = responses.USERNAME_CORRECT_PASSWORD_WRONG
        return did_authenticate

    def save_user(self):
        user = self.get_user()
        if user:
            # user already is in db. try and authenticate
            if self.authenticate(user):
                self.save_current_user(user)
        else:
            # user is not in datbase. let's create one
            self.save_new_user()
        return self.response_number

    def save_current_user(self, user):
        for property in self.user_dict.keys():
            self.save_property(user, property)
        try:
            user.save()
        except Exception:
            response = Response()
            self.response_number = response.FAILED_TO_UPDATE_USER
            pass
        return None

    def save_new_user(self):
        user = User()
        user.date_joined = datetime.datetime.utcnow()
        user.last_login = datetime.datetime.utcnow()
        for user_property in self.user_dict.keys():
            self.save_property(user, user_property)
        try:
            user.save()
        except Exception:
            self.response_number = Response().FAILED_TO_CREATE_USER
        return None

    def save_property(self, user, property_name):
        if property_name == self.property_name.username:
            user.username = self.user_dict[property_name]
        if property_name == self.property_name.password:
            pw_handler = PasswordHandler(self.user_dict[property_name])
            user.password = pw_handler.hash()
        elif property_name == self.property_name.first_name:
            user.first_name = self.user_dict[property_name]
        elif property_name == self.property_name.last_name:
            user.last_name = self.user_dict[property_name]
        elif property_name == self.property_name.is_staff:
            user.is_staff = self.user_dict[property_name]
        elif property_name == self.property_name.is_active:
            user.is_active = self.user_dict[property_name]
        elif property_name == self.property_name.last_login:
            user.last_login = self.date_handler.to_date(self.user_dict[property_name])
        elif property_name == self.property_name.date_joined:
            user.date_joined = self.date_handler.to_date((self.user_dict[property_name]))
        elif property_name == self.property_name.type:
            user.type = self.user_dict[property_name]
        elif property_name == self.property_name.profile_id:
            user.profile_id = self.user_dict[property_name]
        elif property_name == self.property_name.notification_token:
            user.notification_token = self.user_dict[property_name]
        elif property_name == self.property_name.profile_url:
            user.profile_url = self.user_dict[property_name]
        return None

class UserProperties:
    def __init__(self):
        self.username = 'username'
        self.email = 'email'
        self.password = 'password'
        self.first_name = 'first_name'
        self.last_name = 'last_name'
        self.is_staff = 'is_staff'
        self.is_active = 'is_active'
        self.last_login = 'last_login'
        self.date_joined = 'date_joined'
        self.type = 'type'
        self.profile_id = 'profile_id'
        self.notification_token = 'notification_token'
        self.profile_url = 'profile_url'
