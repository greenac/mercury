from sql_interface import UserSqlInterface
from user_model import User
import datetime
from password_handler import PasswordHandler

select_all_single_target = 'select all single target'
insertion = 'insertion'
update = 'update'

target_function = update

user_sql = UserSqlInterface()

if target_function == select_all_single_target:
    results = user_sql.select_all_single_target(type='*',
                                                table='users',
                                                target_column='id',
                                                target_value='7',
                                                match_partial=False
    )

elif target_function == insertion:
    user = User()
    columns = user.properties_list()
    columns = tuple(columns[1:len(columns)])
    date = datetime.datetime.now()
    date_str = '%d-%d-%d %d:%d:%d' % (date.year, date.month, date.day, date.hour, date.minute, date.second)
    pw_handler = PasswordHandler('mypassword')
    hashed_pw = pw_handler.hash()
    values = (hashed_pw,
              date_str,
              0,
              'im_someguy@me.com',
              'this',
              'guy',
              'im_someguy@me.com',
              0,
              0,
              date_str,
              date_str,
              'banter',
              '037363hrbby237348kdi',
              '',
              'some_profile_url',
              'some_profile_pic_url',
    )
    success = user_sql.insert('users', columns, values)
    if success:
        print 'user saved successfully'
    else:
        print 'user was not saved'

elif target_function == update:
    success = user_sql.update(table='users',
                              columns=('first_name', 'last_name'),
                              values=('"alana"', '"garvey"'),
                              target='email',
                              target_value='"acgreen1226@gmail.com"',
                              comparator='='
    )
    if success:
        print 'user updated'
    else:
        print 'failed to update user'