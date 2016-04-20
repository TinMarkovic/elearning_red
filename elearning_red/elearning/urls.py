from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from . import views


app_name = 'elearning'
urlpatterns = [
    url(r'^registration/', views.registration, name='registration'),
    url(r"^courses/edit/(?P<course_id>[0-9]+)", views.course_modify, name="editCourse"),
    url(r"^courses/new", views.course_modify, name="newCourse"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)/block/(?P<block_id>[0-9]+)", views.block_modify, name="editBlock"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)/block/new/(?P<block_type>\w+)", views.block_modify, name="newBlock"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)", views.section_manage, name="manageSection"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/new", views.section_modify, name="newSection"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)$", views.course_manage, name="manageCourse"),
    url(r'^courses/(?P<course_id>[0-9]+)', views.course_show, name="courseView"),
    url(r"^courses/$", views.course_show, name="listCourse"),
    url(r'^user/edit/(?P<customUser_id>[0-9]+)', views.user_modify, name="editUser"),
    url(r'^user/edit/$', views.user_modify, name="createUser"),
    url(r"^programmes/new", views.programme_modify, name="newProgramme"),
    url(r'^programmes/edit/(?P<programme_id>[0-9]+)', views.programme_modify, name="editProgramme"),
    url(r'^programmes/$', views.programmes_show, name='programmesView'),
    url(r'^programmes/(?P<programme_id>[0-9]+)', views.programmes_show, name='programmesListCourses'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r"^courses/list", views.course_show, name="listCourse"),
    url(r'^courses/detail/(?P<course_id>[0-9]+)', views.detail, name="detailCourse"),   
    url(r'^courses/detail/(?P<course_id>[0-9]+)',views.students, name='students'),
    url(r'^addstudents/(?P<course_id>[0-9]+)',views.students, name='students1'),
    url(r'^image/create/$', views.post_create, name='icreate'),
    url(r'^image/create/list$', views.post_list, name='imglist'),
    url(r'^image/show/(?P<id>[0-9]+)', views.post_show, name='ishow'),
    url(r'^image/show/$', views.post_show, name='ishow'),
    url(r'^image/list/$', views.post_list, name='ilist'),
    url(r"^image/edit/(?P<imageblock_id>[0-9]+)", views.post_create, name='iedit'),
    url(r'^video/create/$', views.video_create, name='vcreate'),
    url(r'^video/create/video_list/$', views.video_list, name='vlist'),
    url(r'^home/$', views.homepage, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
