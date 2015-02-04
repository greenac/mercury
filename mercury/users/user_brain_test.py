from user_brain import UserBrain

user_dict = {'password':'im*^%super_&^%tastic',
             'last_login':'1954-6-16 4:55:27',
             'is_superuser':0,
             'username':'superman@krypton.gov',
             'first_name':'Clark',
             'last_name':'Kent',
             'email':'superman@krypton.gov',
             'is_staff':0,
             'is_active':0,
             'date_joined':'1950-7-30 12:45:72',
             'date_updated':'1954-6-16 4:55:27',
             'type':'super',
             'profile_id':'0145256w635e',
             'notification_token':'phone_booth',
             'profile_url':'http://www.upupandaway.com',
             'profile_pic':'superman@krypton.gov.jpeg'
}

ub = UserBrain(user_dict)
print 'user as dict: ' + str(ub.get_user_as_dict())
ub.update_user()
