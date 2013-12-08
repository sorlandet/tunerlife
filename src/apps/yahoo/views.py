from django.utils.http import urlencode
from django.views.generic import ListView
from django.views.generic.edit import FormView

from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class x(ListView):
    pass


class YahooSearchView(FormView):
    template_name = 'yahoo/yahoosearch.html'
    form_class = YahooSearchForm
    initial = {}

    def get(self, request, *args, **kwargs):
        print self.request.GET
        self.initial = self.request.GET
        return super(YahooSearchView, self).get(request, *args, **kwargs)

    # query = None
    # type = 'all'

    def get_context_data(self, **kwargs):
        data = super(YahooSearchView, self).get_context_data(**kwargs)
        # print dir(kwargs['form'])
        print self.initial
        if 'query' in self.initial and self.initial['query']:
            obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
            obj.set_option('query', self.initial['query'])

            obj.set_option('sort', self.initial['sort'])
            obj.set_option('order', self.initial['order'])
            obj.set_option('category', self.initial['category'])
            obj.set_option('item_status', self.initial['item_status'])
            obj.set_option('f', self.initial['f'])
            obj.set_option('output', 'json')
            obj.set_option('store', 0)
            obj.set_option('type', 'all')
            obj.set_option(Search.API_OPTION_PAGE, 0)

            response = obj.action()

            data['jsonp'] = response
            attributes = response['ResultSet']['@attributes']
            result = response['ResultSet']['Result']
            if 'Item' in result:
                data['items'] = result['Item']

            # {u'totalResultsReturned': u'20', u'totalResultsAvailable': u'553', u'firstResultPosition': u'-19'}

            print attributes
        return data