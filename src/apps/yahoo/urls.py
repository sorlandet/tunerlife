from django.conf.urls import patterns, url

from src.apps.yahoo.views import YahooSearchView


urlpatterns = patterns('',
    url(r'search/$', YahooSearchView.as_view(), name='yahoosearch'),
    # url(r'author/(?P<pk>\d+)/$', AuthorUpdate.as_view(), name='author_update'),
    # url(r'author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
)