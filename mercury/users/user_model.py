from date_handler import DateHandler
import datetime

class User:
    def __init__(self):
        self.id = -1
        self.password = ''
        self.last_login = None
        self.is_superuser = False
        self.username = ''
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.is_staff = False
        self.is_active = False
        self.date_joined = None
        self.date_updated = None
        self.type = ''
        self.profile_id = ''
        self.notification_token = ''
        self.profile_url = ''
        self.profile_pic = ''

    def __str__(self):
        return 'username: %s first name: %s last name: %s' % (self.email,
                                                              self.first_name,
                                                              self.last_name)

    def properties(self):
        props = {}
        props_list = self.properties_list()
        for i in range(len(props_list)):
            props[props_list[i]] = i
        return props

    def properties_list(self):
        properties = ['id',
                      'password',
                      'last_login',
                      'is_superuser',
                      'username',
                      'first_name',
                      'last_name',
                      'email',
                      'is_staff',
                      'is_active',
                      'date_joined',
                      'date_updated',
                      'type',
                      'profile_id',
                      'notification_token',
                      'profile_url',
                      'profile_pic'
        ]
        return properties

    def as_dictionary(self):
        date_handler = DateHandler()
        user_dict = {'id':self.id,
                     'password':self.password,
                     'last_login':date_handler.to_string(date=self.last_login),
                     'is_superuser':self.is_superuser,
                     'username':self.username,
                     'first_name':self.first_name,
                     'last_name':self.last_name,
                     'email':self.email,
                     'is_staff':self.is_staff,
                     'is_active':self.is_active,
                     'date_joined':date_handler.to_string(date=self.date_joined),
                     'date_updated':date_handler.to_string(date=self.date_updated),
                     'type':self.type,
                     'profile_id':self.profile_id,
                     'notification_token':self.notification_token,
                     'profile_url':self.profile_url,
                     'profile_pic':self.profile_pic
        }
        return user_dict

    def from_db_data(self, query_result):
        print 'query results sent to user model: ' + str(query_result)
        if query_result:
            user_result = query_result[0]
            if len(user_result) > 0:
                columns = self.properties()
                self.id = user_result[columns['id']]
                self.password = user_result[columns['password']]
                self.last_login = user_result[columns['last_login']]
                self.is_super_user = user_result[columns['is_superuser']]
                self.username = user_result[columns['username']]
                self.first_name = user_result[columns['first_name']]
                self.last_name = user_result[columns['last_name']]
                self.email = user_result[columns['email']]
                self.is_staff = user_result[columns['is_staff']]
                self.is_active = user_result[columns['is_active']]
                self.date_joined = user_result[columns['date_joined']]
                self.date_updated = user_result[columns['date_updated']]
                self.type = user_result[columns['type']]
                self.profile_id = user_result[columns['profile_id']]
                self.notification_token = user_result[columns['notification_token']]
                self.profile_url = user_result[columns['profile_url']]
                self.profile_pic = user_result[columns['profile_pic']]
        return None

    def update_from_dict(self, user_dict):
        self.last_login = datetime.datetime.utcnow()
        self.date_updated = datetime.datetime.utcnow()
        return None