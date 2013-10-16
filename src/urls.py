from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView

import autocomplete_light

from src.apps.article.sitemaps import article_sitemaps
from src.apps.automobile import views as automobile_views
from src.apps.size.sitemaps import size_sitemaps
from src.apps.wheel.sitemaps import wheel_sitemaps

from src.libs.markdown.views import MarkdownTemplateView

autocomplete_light.autodiscover()
admin.autodiscover()

sitemaps = {}
sitemaps.update(article_sitemaps)
sitemaps.update(size_sitemaps)
sitemaps.update(wheel_sitemaps)

urlpatterns = patterns('',
    url(r'^auto/', include('src.apps.automobile.urls', namespace='auto')),

    url(r'^size/', include('src.apps.size.urls', namespace='size')),
    url(r'^tire_calculator/', include('src.apps.tire_calculator.urls',
                                      namespace='tire_calculator')),

    url(r'^articles/', include('src.apps.article.urls')),
    url(r'^contact/', include('src.apps.contacts.urls', namespace='contacts')),

    url(r'^comments/posted/$', automobile_views.CommentsPostedView.as_view()),
    url(r'^comments/', include('django.contrib.comments.urls')),

    url(r'^$', automobile_views.HomeView.as_view(), name='home'),

    url(r'', include('src.apps.wheel.urls', namespace='wheel')),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    url(r'^tinymce/', include('tinymce.urls')),

    url(r'^markdown/preview/$', MarkdownTemplateView.as_view(), name='django_markdown_preview'),
    url(r'^markdown/', include('django_markdown.urls')),

    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^mes_fichiers/', include('src.libs.file_manager.urls',
                                   namespace='mes_fichiers')),
    url(r'^faq/', include('src.libs.faq.urls', namespace='faq')),
    url(r'^banner/', include('src.libs.banner.urls', namespace='banner')),
    url(r'^comments/', include('django.contrib.comments.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

urlpatterns += patterns('django.contrib.sitemaps.views',
    (r'^sitemap\.xml$', 'index', {'sitemaps': sitemaps}),
    (r'^sitemap-(?P<section>.+)\.xml$', 'sitemap', {'sitemaps': sitemaps}),
)

urlpatterns += patterns('',
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name="robots.txt", content_type='text/plain')),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='%s%s' % (settings.STATIC_URL, 'img/icons/favicon.ico'))),
)

# Flatpages as AboutUs, Blog etc
urlpatterns += patterns('django.contrib.flatpages.views',
                        (r'^(?P<url>.*)/$', 'flatpage'),
                        )

# handler500 = 'src.apps.utils.handlers.handler500'