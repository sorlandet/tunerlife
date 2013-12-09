from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView

from src.apps.mixin import JSONViewMixin
from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class YahooSearchView(TemplateView):
    template_name = 'yahoo/yahoosearch.html'


class YahooProcessFormView(ProcessFormView):

    form_class = YahooSearchForm
    initial = {}

    def get(self, request, *args, **kwargs):
        print self.request.GET
        content = self.get_jsonp()
        # print content
        return HttpResponse(content=content,
                            content_type='application/json',
                            status=200)

    def get_jsonp(self):

        obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
        obj.set_option('query', self.request.GET['query'])

        obj.set_option('sort', self.request.GET['sort'])
        obj.set_option('order', self.request.GET['order'])
        obj.set_option('category', self.request.GET['category'])
        obj.set_option('item_status', self.request.GET['item_status'])
        obj.set_option('f', self.request.GET['f'])
        obj.set_option('output', 'json')
        obj.set_option('store', 0)
        obj.set_option('type', 'all')
        obj.set_option(Search.API_OPTION_PAGE, self.request.GET.get('page', 0))

        return obj.action()

        # data['jsonp'] = response
        # attributes = response['ResultSet']['@attributes']
        # result = response['ResultSet']['Result']
        # if 'Item' in result:
        #     data['items'] = result['Item']
        #
        # # {u'totalResultsReturned': u'20', u'totalResultsAvailable': u'553', u'firstResultPosition': u'-19'}
        #
        # print attributes
        # return data