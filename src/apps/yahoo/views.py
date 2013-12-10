from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import ProcessFormView

from src.apps.mixin import JSONViewMixin
from src.apps.yahoo.api import Search
from src.apps.yahoo.forms import YahooSearchForm


class YahooSearchView(TemplateView):
    template_name = 'yahoo/yahoosearch.html'


class YahooProcessFormView(ProcessFormView):

    def get(self, request, *args, **kwargs):

        form = YahooSearchForm(self.request.GET)
        if form.is_valid():
            content = self.get_search_results(form=form)
        else:
            content = ''

        return HttpResponse(content=content, content_type='application/json')

    def get_search_results(self, form):
        page = int(self.request.GET.get('page', 0)) + 1

        obj = Search('dj0zaiZpPXFONUl2dTR2ck5wYyZzPWNvbnN1bWVyc2VjcmV0Jng9YmY-', 'V2')
        obj.set_option('query', form.cleaned_data.get('query'))
        obj.set_option('sort', form.cleaned_data.get('sort', 'end'))
        obj.set_option('order', form.cleaned_data.get('order', 'd'))
        obj.set_option('category', form.cleaned_data.get('category'))
        obj.set_option('item_status', form.cleaned_data.get('item_status'))
        obj.set_option('f', form.cleaned_data.get('f'))
        obj.set_option('output', 'json')
        obj.set_option('store', 0)
        obj.set_option('type', 'all')

        obj.set_option(Search.API_OPTION_PAGE, page)

        return obj.action()