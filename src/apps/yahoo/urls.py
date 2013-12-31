from django.conf.urls import patterns, url

from src.apps.yahoo.views import YahooSearchView, YahooProcessFormView, AuctionLotDetailView


urlpatterns = patterns('',
    url(r'search/$', YahooSearchView.as_view(), name='yahoosearch'),
    url(r'search/ajax/$', YahooProcessFormView.as_view(), name='yahoosearchajax'),
    url(r'search/(?P<AuctionID>.*)/$', AuctionLotDetailView.as_view(), name='auctionlotdetail'),
    # url(r'author/(?P<pk>\d+)/delete/$', AuthorDelete.as_view(), name='author_delete'),
)