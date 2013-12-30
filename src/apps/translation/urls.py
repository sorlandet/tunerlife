from django.conf.urls import patterns, url

from src.apps.translation.views import TranslateProcessFormView


urlpatterns = patterns('',
    url(r'^ajax/$', TranslateProcessFormView.as_view(), name='translation'),
)