from django.conf.urls import patterns, url

from src.libs.banner import views


urlpatterns = patterns('',
    url(r'^click/(?P<banner_id>\d{1,4})/$', views.click, name='banner_click'),
)
