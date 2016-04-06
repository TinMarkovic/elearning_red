from django.conf.urls import url

from . import views

app_name = 'elearning'
urlpatterns = [
    url(r'^$', views.registration, name='registration'),
]
