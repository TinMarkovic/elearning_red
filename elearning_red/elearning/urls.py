from django.conf.urls import url

from . import views

app_name = 'elearning'
urlpatterns = [
    url(r'^registration/', views.registration, name='registration'),
    url(r"^courses/edit/(?P<course_id>[0-9]+)", views.course_modify, name="editCourse"),
    url(r"^courses/new", views.course_modify, name="newCourse"),
    url(r"^courses/list", views.course_show, name="listCourse"),
    url(r'^login/$',views.user_login, name='login'),
]
