from django.conf import settings
from django.views.generic import TemplateView


class MarkdownTemplateView(TemplateView):
    template_name = 'django_markdown/preview.html'

    def get_context_data(self, **kwargs):
        media_or_static = settings.STATIC_URL or settings.MEDIA_URL
        default = media_or_static + 'django_markdown/preview.css'
        css = getattr(settings, 'DJANGO_MARKDOWN_STYLE', default)
        content = self.request.REQUEST.get('data', 'No content posted')

        context = super(MarkdownTemplateView, self).get_context_data(**kwargs)
        context['css'] = css
        context['content'] = content

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)