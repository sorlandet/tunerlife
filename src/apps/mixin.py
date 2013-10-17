# -*- coding: utf-8 -*-
import json
import random

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.cache import patch_response_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
 
 
class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)
 
 
class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
 
 
class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)
 
 
class CacheMixin(object):
    cache_timeout = 60
 
    def get_cache_timeout(self):
        return self.cache_timeout
 
    def dispatch(self, *args, **kwargs):
        return cache_page(self.get_cache_timeout())(super(CacheMixin, self).dispatch)(*args, **kwargs)
 
 
class CacheControlMixin(object):
    cache_timeout = 60
 
    def get_cache_timeout(self):
        return self.cache_timeout
 
    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response
 
 
class JitterCacheMixin(CacheControlMixin):
    cache_range = [40, 80]
 
    def get_cache_range(self):
        return self.cache_range
 
    def get_cache_timeout(self):
        return random.randint(*self.get_cache_range())


class JSONResponse(HttpResponse):
    """
    Return a JSON serialized HTTP resonse
    """
    def __init__(self, request, data, status=200):
        serialized = json.dumps(data)
        super(JSONResponse, self).__init__(
            content=serialized,
            content_type='application/json',
            status=status
        )


class JSONViewMixin(object):
    """
    Add this mixin to a Django CBV subclass to easily return JSON data.
    """
    def json_response(self, data, status=200):
        return JSONResponse(self.request, data, status=200)