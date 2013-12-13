# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView

from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class YahooSearchView(TemplateView):
    template_name = 'yahoo/yahoosearch.html'


class YahooProcessFormView(ProcessFormView):
    category = 2084300257  # Шины, диски

    def get(self, request, *args, **kwargs):

        form = YahooSearchForm(self.request.GET)

        # if self.request.GET.get('f'):
        #     self.f = '0x4'
        # else:
        #     self.f = '0x2'

        if form.is_valid():
            content = self.get_search_results(form=form)
        else:
            content = ''

        return HttpResponse(content=content,
                            content_type='application/json; charset=utf-8')

    def post(self, request, *args, **kwargs):

        form = YahooSearchForm(self.request.POST)

        if form.is_valid():
            content = self.get_search_results(form=form)
        else:
            content = ''

        return HttpResponse(content=content,
                            content_type='application/json; charset=utf-8')


    def get_search_results(self, form):
        page = int(self.request.REQUEST.get('page', 1))

        obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
        obj.set_option('sort', form.cleaned_data.get('sort', 'end'))
        obj.set_option('order', form.cleaned_data.get('order', 'd'))
        obj.set_option('item_status', form.cleaned_data.get('item_status'))
        obj.set_option('f', form.cleaned_data.get('f'))

        aucminprice = form.cleaned_data.get('aucminprice')
        aucmaxprice = form.cleaned_data.get('aucmaxprice')

        print aucminprice, aucmaxprice
        if aucminprice:
            obj.set_option('aucminprice', aucminprice)
        if aucmaxprice:
            obj.set_option('aucmaxprice', aucmaxprice)

        obj.set_option('query', self.get_query(form.cleaned_data.get('query')))
        obj.set_option('category', self.get_category())

        obj.set_option('output', 'json')
        obj.set_option('store', 0)
        obj.set_option('type', 'all')

        obj.set_option(Search.API_OPTION_PAGE, page)

        result = obj.action()

        del obj

        return result

    def get_category(self):
        category = self.request.REQUEST.get('category')
        if category and category.isdigit():
            return category

        ctype = self.request.REQUEST.get('type')

        size = self.request.REQUEST.get('size')
        if size:
            actions = {
                '2084200183': get_wheels,
                '2084005140': get_rims,
            }

            return actions[ctype](size)



        return ctype

    def get_query(self, query):
        mixin = ''
        season = self.request.REQUEST.get('season')

        # print 'season:', season
        if season == 'winter':
            mixin += u'スタッドレス'
        elif season == 'summer':
            mixin += u'-スタッドレス'

        return u' '.join((query, mixin))


def get_wheels(size):
    if size == '17':
        return '2084200189'
    if size == '18':
        return '2084200190'
    if size == '19':
        return '2084200191'


def get_rims(size):
    if size == '17':
        return '2084040548'
    if size == '18':
        return '2084040547'
    if size == '19':
        return '2084195226'