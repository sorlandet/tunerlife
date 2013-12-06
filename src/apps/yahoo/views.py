from django.utils.http import urlencode
from django.views.generic.edit import FormView

from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class YahooSearchView(FormView):
    template_name = 'yahoo/yahoosearch.html'
    form_class = YahooSearchForm
    initial = {}

    def get(self, request, *args, **kwargs):
        self.initial = self.request.GET
        return super(YahooSearchView, self).get(request, *args, **kwargs)

    # query = None
    # type = 'all'

    def get_context_data(self, **kwargs):
        data = super(YahooSearchView, self).get_context_data(**kwargs)
        print dir(kwargs['form'])
        if 'query' in self.initial and self.initial['query']:
            obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
            obj.set_option('query', self.initial['query'])
            obj.set_option('type', self.initial['type'])
            obj.set_option('sort', self.initial['sort'])
            obj.set_option('output', 'json')
            obj.set_option('store', 0)

            response = obj.action()

            data['jsonp'] = response
            data['items'] = response['ResultSet']['Result']['Item']

        return data