from django.db import models
from date_handler import DateHandler

class User(models.Model):
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    type = models.CharField(max_length=30)
    profile_id = models.CharField(max_length=255)
    notification_token = models.CharField(max_length=255)
    profile_url = models.CharField(max_length=255)

    def pic_name(self):
        return self.email + '.jpeg'

    def as_dict(self):
        date_handler = DateHandler()
        user_dict = {'id':self.id,
                     'username':self.username,
                     'first_name':self.first_name,
                     'last_name':self.last_name,
                     'email':self.email,
                     'is_staff':self.is_staff,
                     'is_active':self.is_active,
                     'last_login':date_handler.to_string(date=self.last_login),
                     'date_joined':date_handler.to_string(date=self.date_joined),
                     'type':self.type,
                     'profile_id':self.profile_id,
                     'notification_token':self.notification_token,
                     'profile_url':self.profile_url,
                     'profile_pic':self.pic_name()
        }
        return user_dict