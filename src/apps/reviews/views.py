# -*- coding: utf-8 -*-
import json, os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.core import serializers
from django.core.files import File
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import list_detail


from tunerlife.apps.auto.models import *
from tunerlife.apps.reviews.models import *
from tunerlife.apps.reviews.forms import ReviewForm


REVIEWS_PER_PAGE = settings.REVIEWS_PER_PAGE




@csrf_exempt
def img_uploader(request, **kwargs):
    if request.method == "POST":
        print request.POST
        
        uploadedImage = request.FILES['file']
        print uploadedImage
        
        total = Photo.objects.all().count()
        folder_index = str(total / 1000)
     
#        filename = '%d-%s' % (total + 1, uploadedImage.name)
        filename = uploadedImage.name
        
        image_path = os.path.join('uploaded', folder_index)
        
        upload_full_path = os.path.join(settings.MEDIA_ROOT, image_path)
        
        if not os.path.exists(upload_full_path):
            os.makedirs(upload_full_path)
        
        print request.raw_post_data
        
        dest = open(os.path.join(upload_full_path, filename), 'a')
        for chunk in uploadedImage.chunks(): 
            dest.write(chunk)
        dest.close()
        
        if request.POST.has_key('chunks') and request.POST.has_key('chunk'):
            chunks = int(request.POST['chunks']) - 1
            chunk = int(request.POST['chunk'])
            
            if chunks != chunk: 
                return HttpResponse('')

        p = Photo()
        p.user = request.user
        p.photo = File(open(os.path.join(upload_full_path, filename), 'r'))
        p.save()
        
        ret = json.dumps({'id': p.id, 'tumb': p.get_thumbnail_url(), 'img': p.get_absolute_url()})
        
        return HttpResponse(ret)
    
    
    return HttpResponse('<form enctype="multipart/form-data" method="post" action="/ajax/review/image/uploader/"><input type="file" size="40" name="file"><input type="submit" value="Load" class="submit"></form>')


def tumb_loader(request):
    review_id = request.REQUEST.get('review_id', None)
    
    if not review_id:
        return HttpResponse('') 
    
    print review_id
    pps = ReviewPhoto.objects.filter(review = review_id)
    r = []
    for pp in pps:
        p = pp.photo
        r.append({'id': p.id, 'tumb': p.get_thumbnail_url(), 'img': p.get_absolute_url()})
    print r
    ret = json.dumps(r)
    return HttpResponse(ret) 




@login_required
def add_review(request):
    if request.method == "POST":
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(author = request.user, 
                               creator_ip = request.META['REMOTE_ADDR'], 
                               attached_photos = request.POST['attachedPostPhotos'])
            
            messages.add_message(request, messages.SUCCESS, u"Успешно сохранен review '%s'" % review.title)

            return HttpResponseRedirect(reverse("show_review_by_slug", kwargs = {'review_slug': review.slug}))
        
    else:
        form = ReviewForm()
    
    return render_to_response('reviews/edit.html', { "blog_form": form }, context_instance = RequestContext(request))


def show_review_by_slug(request, review_slug):
    
    review = get_object_or_404(Review, slug = review_slug)
    
    reviews = Review.objects.all()
    
    if not request.user.is_staff or request.user != review.author :
        reviews = reviews.filter(status = Review.PUBLISHED)
    
    extra_context_dic = {}
    
    return list_detail.object_detail(request, queryset = reviews, slug = review_slug,
                    template_object_name = 'review', template_name = 'reviews/item.html',
                    extra_context = extra_context_dic)
    



def show_reviews(request):
    
    reviews = Review.objects.filter(status = Review.PUBLISHED)
    
    extra_context_dic = {}
        
    return list_detail.object_list(request, queryset = reviews, paginate_by = REVIEWS_PER_PAGE,
                    template_object_name = 'review', template_name = 'reviews/list.html',
                    extra_context = extra_context_dic, allow_empty = True)
    
    


@login_required
def edit_review(request, form_class = ReviewForm):

    review_id = request.GET.get('id', None)
    if not review_id:
        raise HTTP404
     
    review = get_object_or_404(Review, id = review_id)
    
    if request.method == "POST":
        
        if review.author != request.user:
            messages.add_message(request, messages.ERROR,
                ugettext("You can't edit reviews that aren't yours")
            )
            return HttpResponse("You can't edit reviews that aren't yours");
#            return HttpResponseRedirect(reverse("blog_list_yours"))

        blog_form = form_class(request.POST)
        if blog_form.is_valid():
            post = blog_form.save(author = request.user, 
                                  creator_ip = request.META['REMOTE_ADDR'], 
                                  attached_photos = request.POST['attachedPostPhotos'], 
                                  review = review)
            
            messages.add_message(request, messages.SUCCESS, u"Успешно сохранен review '%s'" % post.title)
            
            return HttpResponseRedirect(reverse("show_review_by_slug", kwargs = {'review_slug': review.slug}))

        else:
            blog_form = form_class(instance = post)
    else:
        initials = {'body_style': review.body_style,
                    'car_segment': review.car_segment,
                    'car': review.car,
                    'realauthor': review.realauthor,
                    'source': review.source,
                    'title': review.title,
                    'body': review.body,
#                    'geo_tags': post.geo_tags,
                    'tags': review.tags}
        blog_form = form_class(initial = initials)
        
    return render_to_response('reviews/edit.html', { "blog_form": blog_form, "review": review }, context_instance = RequestContext(request))


#
#def dtp_stats(request, maker_slug = None):
#    print maker_slug
#    from django.db.models import Sum
#    extra_context_dic = {}
#    template_name = TEMPLATE_NAME_OF_DTP_STATS_MAKERS
#    
#    if not maker_slug: 
#        makers = RoadTrafficVictims.objects.values('maker__slug', 'maker__name').annotate(Sum('victims'))
#        print makers
#        extra_context_dic['makers'] = makers
#        template_name = TEMPLATE_NAME_OF_DTP_STATS_MAKERS
#    else:
#        maker = get_object_or_404(Maker, slug = maker_slug)
#        extra_context_dic['maker'] = maker
#        lines = RoadTrafficVictims.objects.values('line__slug', 'line__name').filter(maker = maker).annotate(Sum('victims'))
#        print lines 
#        extra_context_dic['lines'] = lines
#        template_name = TEMPLATE_NAME_OF_DTP_STATS_LINES
#    
#    return render_to_response(template_name, extra_context_dic, context_instance = RequestContext(request))