from django.utils.http import urlencode
from django.views.generic.edit import FormView

from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class YahooSearchView(FormView):
    template_name = 'yahoo/yahoosearch.html'
    form_class = YahooSearchForm

    def post(self, request, *args, **kwargs):
        print 'post'
        return super(YahooSearchView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print 'get'
        return super(YahooSearchView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(YahooSearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get('query')

        if query:
            obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
            obj.set_option('query', query)
            obj.set_option('output', 'json')

            response = obj.action()

            data['jsonp'] = response
            data['items'] = response['ResultSet']['Result']['Item']

        return data






