# -*- coding: utf-8 -*-

import re
#from datetime import datetime

from django import forms

from tagging.forms import TagField 

from tunerlife.apps.reviews.models import Review, Photo, ReviewPhoto
from tunerlife.apps.auto.models import BodyStyle, CarSegment

TEASE_TEXT_LENGTH = 500
TEASE_BREAK = '<hr class="teasebreak" />'

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_extra_spaces(data):
    p = re.compile(r'\s+')
    return p.sub(' ', data)

class ReviewForm(forms.Form):
    
    body_style = forms.ModelChoiceField(queryset = BodyStyle.objects.all(), empty_label = 'Выберите тип кузова')
    car_segment = forms.ModelChoiceField(queryset = CarSegment.objects.all(), empty_label = 'Выберите сегмент')
    
    car = forms.CharField(required = False, max_length = 60)
    
    realauthor = forms.CharField(required = False, max_length = 200)
    source = forms.CharField(required = False, max_length = 200)
    
    title = forms.CharField(required = False, max_length = 60, min_length = 10)
    body = forms.CharField(required = False, widget = forms.Textarea())

#    tease = forms.CharField(required = False, widget = forms.Textarea(attrs = {'cols': 70, 'rows': 5 }), label = 'Аннотация')

    tags = TagField(required = False, label = 'Тэги')
    
    
    def clean_body(self):
        data = self.cleaned_data['body']
        
        if TEASE_BREAK not in data:
            cleaned = remove_extra_spaces(remove_html_tags(data))
            
            if len(cleaned) > TEASE_TEXT_LENGTH:
                raise forms.ValidationError(u"Пожалуйста добавьте разрыв страницы, для определения аннотации.")
            else:
                # text part of the body is ok
                # check body for "application/x-shockwave-flash" objects and <img>

                p_end = data.find('</p>') + 4
                
                self.tease = data[0:p_end]
                
                p_of_object_end = data.find('</p>', data.find('</object>')) + 4
                p_of_img_end = data.find('</p>', data.find('<img ')) + 4
                
                
                if (p_end < p_of_object_end) or (p_end < p_of_img_end):
                    if p_of_object_end != -1 and p_of_img_end != -1:
                        if p_of_img_end < p_of_object_end: 
                            self.tease = data[0:p_of_img_end]
                        else:
                            self.tease = data[0:p_of_object_end]
                    elif p_of_object_end != -1 and p_of_img_end == -1:
                        self.tease = data[0:p_of_object_end]
                    elif p_of_object_end == -1 and p_of_img_end != -1:
                        self.tease = data[0:p_of_img_end]
                else:
                    p2_of_object_end = data.find('</p>', data.find('</object>'), p_of_object_end) + 4
                    p2_of_img_end = data.find('</p>', data.find('<img '), p_of_img_end) + 4
                    if p2_of_object_end == -1 and p2_of_img_end == -1:
                        self.tease = data
        else:
            tbr = data.find(TEASE_BREAK)
            cleaned = remove_extra_spaces(remove_html_tags(data[0:tbr]))
            if len(cleaned) > TEASE_TEXT_LENGTH:
                raise forms.ValidationError(u"Пожалуйста установите разрыв страницы, для определения аннотации, выше по тексту.")
            
            data = data[0:tbr]
            
            p_end = data.find('</p>') + 4
                
            self.tease = data[0:p_end]
            
            p_of_object_end = data.find('</p>', data.find('</object>')) + 4
            p_of_img_end = data.find('</p>', data.find('<img ')) + 4
            
            
            if (p_end < p_of_object_end) or (p_end < p_of_img_end):
                if p_of_object_end != -1 and p_of_img_end != -1:
                    if p_of_img_end < p_of_object_end: 
                        self.tease = data[0:p_of_img_end]
                    else:
                        self.tease = data[0:p_of_object_end]
                elif p_of_object_end != -1 and p_of_img_end == -1:
                    self.tease = data[0:p_of_object_end]
                elif p_of_object_end == -1 and p_of_img_end != -1:
                    self.tease = data[0:p_of_img_end]
            else:
                p2_of_object_end = data.find('</p>', data.find('</object>'), p_of_object_end) + 4
                p2_of_img_end = data.find('</p>', data.find('<img '), p_of_img_end) + 4
                if p2_of_object_end == -1 and p2_of_img_end == -1:
                    self.tease = data
            
        return self.cleaned_data['body']
    
    
    def save(self, **kwargs):
        
        if kwargs.has_key('review'):
            review = kwargs.get('review')
        else:
            review = Review()
        
        review.author = kwargs.get('author', None)
        review.body_style = self.cleaned_data.get('body_style')
        review.car_segment = self.cleaned_data.get('car_segment')
        
        review.car = self.cleaned_data.get('car')
        
        review.title = self.cleaned_data.get('title')
        
        review.realauthor = self.cleaned_data.get('realauthor')
        review.source = self.cleaned_data.get('source')
        
        review.creator_ip = kwargs.get('creator_ip', '0.0.0.0')
        
        review.body = self.cleaned_data.get('body')
        
        review.tease = self.tease
        
        review.tags = self.cleaned_data.get('tags')
    
        review.save()
        

            
        if kwargs.get('attached_photos', None):
            photos_ids = [int(id) for id in kwargs['attached_photos'].split(',')]
        else:
            photos_ids = []
        
        print "Attached photos: ", photos_ids
        
        pps = ReviewPhoto.objects.filter(review = review)
        need_to_delete = list(pps.values_list('review', flat = True))
        for i in photos_ids:
            try:
                need_to_delete.remove(i)
            except ValueError:
                pass 

#        print photos_ids, need_to_delete 
        pps.delete()
        
        Photo.objects.filter(id__in = list(need_to_delete)).delete()
        
        for photo_id in photos_ids:
            obj, created = ReviewPhoto.objects.get_or_create(review = review, photo = Photo.objects.get(id = photo_id))
            
        return review
        


        

    