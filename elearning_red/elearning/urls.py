from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


app_name = 'elearning'
urlpatterns = [
    url(r'^registration/', views.registration, name='registration'),
    url(r"^courses/edit/(?P<course_id>[0-9]+)", views.course_modify, name="editCourse"),
    url(r"^courses/new", views.course_modify, name="newCourse"),
    url(r"^courses/list/$", views.course_show, name="listCourse"),
    url(r'^courses/(?P<course_id>[0-9]+)', views.course_show),
   #TODO: url(r'courses/list/(?P<course_id>[0-9]+)' views.course_details name='course details')
    url(r'^user/edit/(?P<customUser_id>[0-9]+)', views.user_modify, name="editUser"),
    url(r'^user/edit/$', views.user_modify, name="createUser"),
    url(r"^programmes/new", views.programme_modify, name="newProgramme"),
    url(r'^programmes/edit/(?P<programme_id>[0-9]+)', views.programme_modify, name="editProgramme"),
    url(r'^programmes/$', views.programmes_show, name='programmesView'),
    url(r'^programmes/(?P<programme_id>[0-9]+)', views.programmes_show, name='programmesListCourses'),
    #url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^courses/list/(?P<course_id>[0-9]+)', views.course_show, name="courseView"),
    url(r'^HTMLBlocks/edit/(?P<HTMLBlock_id>[0-9]+)', views.HTMLBlock_modify, name="editBlock"),
    url(r'^HTMLBlocks/edit/$', views.HTMLBlock_modify, name="editBlock"),
    url(r'^HTMLBlocks/(?P<HTMLBlock_id>[0-9]+)', views.HTMLBlock_show, name="showBlock"),
    #radni url:
    url(r'^HTMLBlocks/$', views.HTMLBlock_show, name="showBlock"),
    url(r'^login/$', auth_views.login),
    url(r'^password-change/$', auth_views.password_change, {'template_name': 'change-password.html'}, name='password_change'),
    url(r'^password-change-done/$', auth_views.password_change_done, {'template_name': 'password_change-password.html'}, name='password_change_done'),
]
