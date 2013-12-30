from django.db import models


class Translation(models.Model):
    source_lang = models.CharField(max_length=15)
    target_lang = models.CharField(max_length=15)

    original = models.CharField(max_length=250)
    translated = models.CharField(max_length=250)
