# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import smart_unicode

from tagging.fields import TagField

class BodyStyle(models.Model):
    class Meta:
        verbose_name = u"Тип автомобильного кузова"
        verbose_name_plural = u"Типы автомобильных кузовов"
        ordering = ["name"]
    
    CLOSED_BODY = 1
    OPEN_BODY = 2
    UTILITY_BODY = 3
    
    TYPE_CHOICES = (
        (CLOSED_BODY,    u"Закрытые"),
        (OPEN_BODY,      u"Открытые"),
        (UTILITY_BODY,   u"Грузопассажирские"),
    )
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, db_index=True)
    type = models.IntegerField(choices=TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    tags = TagField()
    
    def __unicode__(self):
        return smart_unicode(self.name)
    
    
class CarSegment(models.Model):
    class Meta:
        verbose_name = u"Тип сегмента"
        verbose_name_plural = u"Типы автомобильных сегментов"
        ordering = ["name"]
        
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    
    tags = TagField()
    
    def __unicode__(self):
        return smart_unicode(self.name)