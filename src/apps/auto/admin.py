# -*- coding: utf-8 -*-

from django.contrib import admin
from src.apps.auto.models import BodyStyle, CarSegment

class BodyStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'type')
    list_filter = ('type', )
    prepopulated_fields = {"slug": ("name",)}

class CarSegmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}



admin.site.register(BodyStyle, BodyStyleAdmin)
admin.site.register(CarSegment, CarSegmentAdmin)