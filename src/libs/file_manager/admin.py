from django.contrib import admin

from src.libs.file_manager.models import MonFichier, MonAlbum


class MonFichierAdmin(admin.ModelAdmin):
    pass


class MonAlbumAdmin(admin.ModelAdmin):
    pass


admin.site.register(MonFichier, MonFichierAdmin)
admin.site.register(MonAlbum, MonAlbumAdmin)