from django.conf.urls import patterns, url

from src.apps.yahoo.views import YahooSearchView, YahooProcessFormView


urlpatterns = patterns('',
    url(r'search/$', YahooSearchView.as_view(), name='yahoosearch'),
    url(r'search/ajax/$', YahooProcessFormView.as_view(), name='yahoosearchajax'),
    # url(r'author/(?P<pk>\d+)/$', AuthorUpdate.as_view(), name='author_update'),
    # url(r'author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
)