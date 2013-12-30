from django.contrib import admin

from src.apps.translation.models import Translation


class TranslationAdmin(admin.ModelAdmin):
    list_display = ["original", "translated", "source_lang", "target_lang"]


admin.site.register(Translation, TranslationAdmin)