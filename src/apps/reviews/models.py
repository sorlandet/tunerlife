# -*- coding: utf-8 -*-

import os, datetime

from django.db import models
 
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from tagging.fields import TagField
from tagging.models import Tag

from threadedcomments.models import ThreadedComment

from src.apps import utils
from src.apps.auto.models import BodyStyle, CarSegment
from src.apps.reviews.utils import create_thumbnail, delete_thumbnail, get_thumbnail_url



class Review(models.Model):
    class Meta:
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"

    DRAFT = 1
    PUBLISHED = 2
    DELETED = 3
    
    STATUS_CHOICES = (
        (DRAFT,     u"Черновик"),
        (PUBLISHED, u"Опубликовано"),
        (DELETED,   u"Удалено"),
    )
    
    author = models.ForeignKey(User)
    
    body_style  = models.ForeignKey(BodyStyle)
    car_segment = models.ForeignKey(CarSegment)
    
    car = models.CharField(blank = True, max_length = 60)
    
    title = models.CharField(_("title"), max_length = 60)
    slug = models.SlugField(max_length = 64, db_index = True)
    
    realauthor = models.CharField(blank = True, max_length = 200, help_text = u"Имя автора оригинала")
    source = models.CharField(blank = True, max_length = 200, help_text = u"Источник (ссылка на оригинал)")
    
    creator_ip = models.IPAddressField(blank = True, null = True, help_text = u"IP адрес создателя записи") 
    
    body = models.TextField()
    tease = models.TextField(blank = True)
    
    allow_comments = models.BooleanField(default = True)
    
    tags = TagField()
    
    status = models.IntegerField(choices = STATUS_CHOICES, default = DRAFT)

    published = models.DateTimeField(null = True, blank = True, help_text = "Дата написания")
    created = models.DateTimeField(auto_now_add = True, help_text = u'Создано')
    updated = models.DateTimeField(auto_now = True, help_text = u'Обновлено')
    
    def __unicode__(self):
        return u'%s' % self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            utils.unique_slugify(self, self.title)
            self.published = datetime.datetime.today()
        self.updated = datetime.datetime.today()
        
        super(Review, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return '/review/%s/' % self.slug
    
    
    def comments_count(self):
        review_type = ContentType.objects.get_for_model(Review)
        return ThreadedComment.objects.filter(content_type = review_type, object_id = self.id).count()
    
    def get_tags(self):
        return Tag.objects.get_for_object(self) 
    





def get_image_path(instance, filename):
    
    filename = os.path.basename(filename)
    
    from tunerlife.apps.reviews.models import Photo
    total = Photo.objects.all().count()
    folder_index = str(total / 1000)
     
    filename = '%d-%s' % (total + 1, filename)
    return os.path.join('reviewphotos', folder_index, filename)

    
class Photo(models.Model):
    user = models.ForeignKey(User, related_name = 'photos')
    photo = models.ImageField(upload_to = get_image_path)
    creation_date = models.DateTimeField(auto_now_add = True)
    
    def get_absolute_url(self):
        return self.photo.url

    def get_thumbnail_url(self):
        return get_thumbnail_url(self.photo.url, 120)
    
    def get_upload_to(self):
        return self.user.username



class ReviewPhoto(models.Model):
    review = models.ForeignKey(Review)
    photo = models.ForeignKey(Photo)    
    
    
         
def review_photo_save_handler(sender, **kwargs):
    instance = kwargs['instance']
    create_thumbnail(instance.photo.path, 120, 90)

def review_photo_pre_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    delete_thumbnail(instance.photo.path, 120)

models.signals.post_save.connect(review_photo_save_handler, sender = Photo)
models.signals.pre_delete.connect(review_photo_pre_delete_handler, sender = Photo) 



