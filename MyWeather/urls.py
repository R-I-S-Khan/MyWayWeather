from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.myWeather,name='myWeather'),
    url(r'userRequest/$', views.userRequest,name='userRequest'),

]