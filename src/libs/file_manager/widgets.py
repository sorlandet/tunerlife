from __future__ import unicode_literals

from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe


class FileManagerRawIdWidget(ForeignKeyRawIdWidget):

    def render(self, name, value, attrs=None):
        rel_to = self.rel.to
        if attrs is None:
            attrs = {}
        extra = []
        if rel_to in self.admin_site._registry:
            related_url = reverse('mes_fichiers:index')
            params = self.url_parameters()
            if params:
                url = '?' + '&amp;'.join(['%s=%s' % (k, v) for k, v in params.items()])
            else:
                url = ''
            if "class" not in attrs:
                attrs['class'] = 'vForeignKeyRawIdAdminField' # The JavaScript code looks for this hook.
            # TODO: "lookup_id_" is hard-coded here. This should instead use
            # the correct API to determine the ID dynamically.
            extra.append('<a href="%s%s" class="related-lookup" id="lookup_id_%s" onclick="return showRelatedObjectLookupPopup(this);"> '
                         % (related_url, url, name))
            extra.append('<img src="%s" width="16" height="16" alt="%s" /></a>'
                         % (static('admin/img/selector-search.gif'), _('Lookup')))
        output = [super(ForeignKeyRawIdWidget, self).render(name, value, attrs)] + extra
        if value:
            output.append(self.label_for_value(value))
        return mark_safe(''.join(output))

    def url_parameters(self):
        params = super(FileManagerRawIdWidget, self).url_parameters()
        params.update({'django_foreign_key': True})
        return params