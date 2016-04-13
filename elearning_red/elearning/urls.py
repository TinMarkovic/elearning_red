from django.conf.urls import url

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
    url(r"^programme/new", views.programme_modify, name="newProgramme"),
    url(r'^programme/edit/(?P<prorgamme_id>[0-9]+)', views.programme_modify, name="editProgramme"),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^courses/list/(?P<course_id>[0-9]+)', views.course_show, name="courseView")  
]
