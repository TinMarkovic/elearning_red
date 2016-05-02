from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views


app_name = 'elearning'
urlpatterns = [
    url(r'^ajax/modify-block-order/(?P<course_id>[0-9]+)', views.section_reorder_blocks, name='sectionReorderBlocks'),
    url(r'^ajax/modify-section-order/(?P<course_id>[0-9]+)', views.course_reorder_sections, name='courseReorderSections'),
    url(r'^ajax/get-blocks-list/(?P<course_id>[0-9]+)', views.section_list_blocks, name='sectionListBlocks'),
    
    url(r'^manage/courses/(?P<course_id>[0-9]+)/students', views.course_students, name='manageStudents'),
    url(r"^manage/courses/(?P<course_id>[0-9]+)/sections/(?P<section_id>[0-9]+)/blocks/edit/(?P<block_id>[0-9]+)", views.block_modify, name="editBlock"),
    url(r"^manage/courses/(?P<course_id>[0-9]+)/sections/(?P<section_id>[0-9]+)/blocks/new/(?P<block_type>\w+)", views.block_modify, name="newBlock"),
    url(r"^manage/courses/(?P<course_id>[0-9]+)/sections/(?P<section_id>[0-9]+)", views.section_manage, name="manageSection"),
    url(r"^manage/courses/(?P<course_id>[0-9]+)/sections/edit/(?P<section_id>[0-9]+)", views.section_modify, name="editSection"),
    url(r"^manage/courses/(?P<course_id>[0-9]+)/sections/new", views.section_modify, name="newSection"),
    url(r"^manage/courses/(?P<course_id>[0-9]+)$", views.course_manage, name="manageCourse"),
    url(r"^manage/courses/edit/(?P<course_id>[0-9]+)", views.course_modify, name="editCourse"),
    url(r"^manage/courses/new", views.course_modify, name="newCourse"),
    
    url(r"^courses/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)/block/(?P<block_id>[0-9]+)/quiz", views.block_quiz, name="showQuiz"),
    url(r"^courses/(?P<course_id>[0-9]+)/section/(?P<section_id>[0-9]+)", views.blocks_studentview, name="showBlocks"),
    url(r'^courses/(?P<course_id>[0-9]+)/students', views.course_show, name="showStudentsInCourse"),
    url(r'^courses/(?P<course_id>[0-9]+)', views.course_show, name="showCourse"),
    url(r"^courses", views.course_show, name="listCourses"),
    
    url(r'^manage/programmes/(?P<programme_id>[0-9]+)/students', views.programme_students, name='manageStudentsProgramme'),
    url(r'^manage/programmes/(?P<programme_id>[0-9]+)/courses', views.programme_manage, name='manageCoursesProgramme'),
    url(r"^manage/programmes/new", views.programme_modify, name="newProgramme"),
    url(r'^manage/programmes/(?P<programme_id>[0-9]+)', views.programme_modify, name="editProgramme"),
    
    url(r'^programmes/(?P<programme_id>[0-9]+)', views.programmes_show, name='showProgramme'),
    url(r'^programmes/', views.programmes_show, name='listProgrammes'),
    
    url(r'^users/edit/(?P<customUser_id>[0-9]+)', views.user_modify, name="editUser"),
    url(r'^users/edit', views.user_create, name="createUser"),
    url(r'^users/profile', views.user_profile, name="userProfile"),
    url(r'^users/', views.users_list, name="listUsers"),
    

    url(r'^logout', views.user_logout, name='logout'),
    url(r'^about', views.about, name='about'),
    
    url(r'^$', views.homepage, name='homepage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
