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

#url(r'^blocks/imagecreate/$', views.post_create, name='imagecreate'),
#url(r'^$', RedirectView.as_view(url='list', permanent=True)),