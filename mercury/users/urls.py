from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
                       url(r'^get_user/', views.get_user),
                       url(r'^save_user/', views.save_user),
                       url(r'^all_users/', views.all_users),
)