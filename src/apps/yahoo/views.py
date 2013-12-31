# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView
import jsonpickle

from src.apps.yahoo.api import Search, AuctionItem
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
            print 'valid form'
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
        obj.set_option('item_status', form.cleaned_data.get('item_status', 0))

        buynow = form.cleaned_data.get('buynow')
        if buynow:
            obj.set_option('buynow', 1)

        aucminprice = form.cleaned_data.get('aucminprice')
        aucmaxprice = form.cleaned_data.get('aucmaxprice')

        print aucminprice, aucmaxprice
        if aucminprice:
            obj.set_option('aucminprice', aucminprice)
        if aucmaxprice:
            obj.set_option('aucmaxprice', aucmaxprice)

        query = form.cleaned_data.get('query')
        obj.set_option('query', self.get_query(query))
        obj.set_option('category', self.get_category())

        obj.set_option('output', 'json')
        obj.set_option('store', 0)
        obj.set_option('type', 'all')
        obj.set_option('f', '0x4')

        obj.set_option(Search.API_OPTION_PAGE, page)

        result = obj.action()

        # data = json.loads(result)
        # if data['ResultSet']['Result']['Item']:
        #     items = list(data['ResultSet']['Result']['Item'])
        #     for item in items:
        #         item['TitleRus'] = translate('ja', 'ru', smart_unicode(item['Title']))
        # return json.dumps(data)
        return result

    def get_category(self):
        category = self.request.POST.get('category')
        if category and category.isdigit():
            return category

        ctype = self.request.POST.get('type')

        size = self.request.POST.get('size')
        if size:
            actions = {
                '2084200183': get_wheels,
                '2084005140': get_rims,
            }

            return actions[ctype](size)



        return ctype

    def get_query(self, query):
        mixins = [query, ]

        widths = self.request.POST.getlist('width')
        widths = ' '.join([el for el in widths if el])
        if widths:
            width_mixin = '(%s)J' % widths
            print 'width_mixin:', width_mixin
            mixins.append(width_mixin)

        bolt_pattern = self.request.POST.get('bolt_pattern')
        if bolt_pattern:
            print 'bolt pattern:', bolt_pattern
            holes, pcd = bolt_pattern.split('x')
            bolt_pattern_mixin = u'%s穴 %s' % (holes, pcd)
            mixins.append(bolt_pattern_mixin)

        offsets = self.request.POST.getlist('offset')
        offsets_pos = ' '.join([el.strip('+') for el in offsets if el and '+' in el])
        offsets_neg = ' '.join([el.strip('-') for el in offsets if el and '-' in el])
        if offsets_pos:
            print 'offsets_pos:', offsets_pos
            offset_pos_mixin = '+(%s)' % offsets_pos
            print 'offset_pos_mixin:', offset_pos_mixin
            mixins.append(offset_pos_mixin)

        if offsets_neg:
            print 'offsets_neg:', offsets_neg
            offsets_neg_mixin = '-(%s)' % offsets_neg
            print 'offsets_neg_mixin:', offsets_neg_mixin
            mixins.append(offsets_neg_mixin)

        season = self.request.REQUEST.get('season')
        print 'season:', season
        if season == 'winter':
            mixins.append(u'スタッドレス')
        elif season == 'summer':
            mixins.append(u'-スタッドレス')

        return u' '.join(mixins)


class AuctionLotDetailView(TemplateView):
    template_name = 'yahoo/auctionlot_detail.html'
    auction_id_url_kwarg = 'AuctionID'

    def get_object(self):
        auction_id = self.kwargs.get(self.auction_id_url_kwarg, None)

        obj = AuctionItem('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
        obj.set_option(AuctionItem.API_OPTION_AUCTIONID, auction_id)
        obj.set_option('output', 'json')

        return obj.action()

    def get_context_data(self, **kwargs):
        context = super(AuctionLotDetailView, self).get_context_data(**kwargs)
        decoded_response = jsonpickle.decode(self.get_object(), keys=True)
        lot = auction_item_decoder(decoded_response['ResultSet']['Result'])
        context['lot'] = lot
        return context


class AuctionLot(object):
    pass


class Seller(object):
    pass


def auction_item_decoder(obj):
    lot = AuctionLot()
    lot.AuctionID = obj['AuctionID']
    lot.CategoryID = obj['CategoryID']
    lot.Title = obj['Title']

    seller = Seller()
    seller.Id = obj['Seller']['Id']
    seller.Rating = obj['Seller']['Rating']
    seller.ItemListURL = obj['Seller']['ItemListURL']
    seller.RatingURL = obj['Seller']['RatingURL']

    lot.Seller = seller
    lot.AuctionItemUrl = obj['AuctionItemUrl']

    images = []
    for key in obj['Img']:
        images.append(obj['Img'][key])

    lot.Images = images


    # print obj
    # obj['ResultSet']

    return lot

def get_wheels(size):
    if size == '16':
        return '2084200188'
    if size == '17':
        return '2084200189'
    if size == '18':
        return '2084200190'
    if size == '19':
        return '2084200191'
    if size == '20':
        return '2084200192'


def get_rims(size):
    if size == '16':
        return '2084008474'
    if size == '17':
        return '2084040548'
    if size == '18':
        return '2084040547'
    if size == '19':
        return '2084195226'
    if size == '20':
        return '2084195227'
