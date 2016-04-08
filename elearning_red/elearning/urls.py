from django.conf.urls import url

from . import views

app_name = 'elearning'
urlpatterns = [
    url(r'^registration/', views.registration, name='registration'),
    url(r'^courses/', views.courses, name='courses'),
]
