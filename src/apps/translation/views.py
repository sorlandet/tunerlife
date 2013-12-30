import json
import re
import urllib
import urllib2

from django.http import HttpResponse
from django.utils.encoding import smart_unicode
from django.views.generic.edit import ProcessFormView

from src.apps.translation.models import Translation


class TranslateProcessFormView(ProcessFormView):
    target_lang = 'en'
    source_lang = 'auto'
    text = ''

    def get(self, request, *args, **kwargs):

        self.target_lang = self.request.GET.get('tl', 'en')
        self.source_lang = self.request.GET.get('sl', 'auto')
        self.text = self.request.GET.get('title', '')

        trans, created = Translation.objects.get_or_create(
            source_lang=self.source_lang,
            target_lang=self.target_lang,
            original=self.text,
            defaults={'translated': self.translate_by_google()})
        print created

        return HttpResponse(content=trans.translated)

    def translate_by_google(self):
        """
        Translates a given text from
        source language (sl) to target language (tl)
        """

        opener = urllib2.build_opener()
        opener.addheaders = [
            ('User-agent',
             'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)')
        ]

        data = urllib.urlencode(
            {'ie': 'UTF8',
             'text': self.text.encode('utf-8'),
             'sl': self.source_lang,
             'tl': self.target_lang
            }
        )
        params = urllib.urlencode({'client': 't'})
        url = "http://translate.google.com/translate_a/t?" + params

        try:
            response = opener.open(url, data=data)
            res = smart_unicode(response.read())
            fixed_json = re.sub(r',{2,}', ',', res).replace(',]', ']')
            data = json.loads(fixed_json)
            return "%s" % data[0][0][0]
        except urllib2.HTTPError, e:
            print e.code
        except urllib2.URLError, e:
            print e.args

        return ''