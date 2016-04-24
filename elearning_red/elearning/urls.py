from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views


app_name = 'elearning'
urlpatterns = [
    url(r'^ajax/modify-block-order/', views.section_reorder_blocks, name='section_reorder_blocks'),
    url(r'^ajax/modify-section-order/', views.course_reorder_sections, name='course_reorder_sections'),
    url(r'^ajax/get-blocks-list/', views.section_list_blocks, name='section_list_blocks'),
    url(r'^registration/', views.registration, name='registration'),
    url(r"^courses/edit/(?P<course_id>[0-9]+)", views.course_modify, name="editCourse"),
    url(r"^courses/new", views.course_modify, name="newCourse"),
    url(r'^courses/manage/(?P<course_id>[0-9]+)/students', views.course_students, name='manageStudents'),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)/block/(?P<block_id>[0-9]+)", views.block_modify, name="editBlock"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)/block/new/(?P<block_type>\w+)", views.block_modify, name="newBlock"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)", views.section_manage, name="manageSection"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)/section/new", views.section_modify, name="newSection"),
    url(r"^courses/manage/(?P<course_id>[0-9]+)$", views.course_manage, name="manageCourse"),
    url(r'^courses/(?P<course_id>[0-9]+)/details', views.course_details, name="detailsCourse"),
    url(r'^courses/(?P<course_id>[0-9]+)', views.course_show, name="courseView"),
    url(r"^courses/$", views.course_show, name="listCourse"),
    url(r'^user/edit/(?P<customUser_id>[0-9]+)', views.user_modify, name="editUser"),
    url(r'^user/edit/$', views.create_user, name="createUser"),
    url(r"^programmes/new", views.programme_modify, name="newProgramme"),
    url(r'^programmes/edit/(?P<programme_id>[0-9]+)', views.programme_modify, name="editProgramme"),
    url(r'^programmes/$', views.programmes_show, name='programmesView'),
    url(r'^programmes/(?P<programme_id>[0-9]+)', views.programmes_show, name='programmesListCourses'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^$', views.homepage, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
