# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from tunerlife.apps.reviews import views
#from lentadtp.apps.blog.forms import *
#from lentadtp.apps.blog.views import tags, with_tag


urlpatterns = patterns("",
#    url(r'^tags/$', tags, name="blog_tags"),
#    url(r'^tag/(?P<tag>[^/]+)/$', with_tag, name="blog_tag"), 
#    url(r'^tag/(?P<tag>[^/]+)/page/(?P<page>d+)/$', with_tag, name="blog_tag"),
        
    # Add new Car review
    url(r"^review/add/$", views.add_review, name = "add_review"),
    
    # Edit Car review
    url(r"^review/edit/$", views.edit_review, name="edit_review"),
    
    # Car review (item)
    url(r"^review/(?P<review_slug>[-\w]+)/$", views.show_review_by_slug, name="show_review_by_slug"),
    
    # Car review (list)
    url(r"^reviews/$", views.show_reviews, name = "show_reviews"),

    #Image uploader
    url(r'^ajax/review/image/uploader/$', views.img_uploader),
    #JSON tumbnails loader
    url(r'^ajax/review/image/tumbloader/$', views.tumb_loader),                                   
)
