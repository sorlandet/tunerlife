# -*- coding: utf-8 -*-

from django.contrib import admin

from tunerlife.apps.reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["title", "published", "creator_ip", "allow_comments", "status"]
    list_filter = ["published", "status"]
    search_fields = ["title", "body", "tease"]

admin.site.register(Review, ReviewAdmin)