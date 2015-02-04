from sql_interface import UserSqlInterface
from user_model import User
from date_handler import DateHandler
from user_model import User
from response import Response
from password_handler import PasswordHandler

class UserBrain:
    def __init__(self, user_dict):
        self.user_dict = user_dict
        self.sql_interface = UserSqlInterface(host='localhost',
                                              database='users_db',
                                              user='andre',
                                              password='Perhar@6221')
        self.users_table = 'users'
        self.response = Response()
        self.is_new_user = self.user_dict['is_new_user']

    def username(self):
        return self.user_dict['username']

    def is_user_in_db(self, username):
        user = self.get_user_from_db_for_username()
        if user:
            return True
        return False

    def get_user_from_db_for_username(self):
        value = """"%s""""" % self.username()
        results = self.sql_interface.select_all_single_target(type='*',
                                                              table=self.users_table,
                                                              target_column='username',
                                                              target_value=value
        )
        print 'results' + str(results)
        user = User()
        user.from_db_data(results)
        print str(user)
        return user

    def get_user(self):
        user = self.get_user_from_db_for_username()
        if user:
            return user.as_dictionary()
        return {'response':self.response.USER_DOES_NOT_EXIST}

    def process_user(self):
        if self.is_new_user:
            print 'no user'
            success = self.sql_interface.insert(table=self.users_table,
                                                columns=tuple(self.user_dict.keys()),
                                                values=tuple(self.user_dict.values())
            )
            if success:
                # user successfully created
                response_code = self.response.NEW_USER_CREATED
            else:
                response_code = self.response.FAILED_TO_CREATE_USER
        else:
            response_code = self.update_user()
        return response_code

    def get_property_or_return_none(self, dictionary, key):
        try:
            value = dictionary[key]
        except KeyError:
            value = None
        return value

    def update_user(self):
        # check if passwords match
        password = self.user_dict['password']
        pw_handler = PasswordHandler(pw_plain_text=password)
        if pw_handler.authenticate():
            user = self.get_user_from_db_for_username()
            user.update_from_dict(self.user_dict)
            date_handler = DateHandler()
            success = self.sql_interface.update(table='users',
                                                columns=('last_login', 'date_updated'),
                                                values=(),
                                                target='id',
                                                target_value=str(date_handler.to_string(date=user.last_login),
                                                                 date_handler.to_string(date=user.date_updated)),
                                                comparator='='
            )
            if success:
                return self.response.USERNAME_AND_PASSWORD_CORRECT
            else:
                return self.response.FAILED_TO_UPDATE_USER
        else:
            return self.response.USERNAME_CORRECT_PASSWORD_WRONG
