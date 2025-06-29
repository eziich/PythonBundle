from django.contrib import admin
from . import models

admin.site.register(models.Profile)
admin.site.register(models.Follow)
admin.site.register(models.Media)
admin.site.register(models.Like)
admin.site.register(models.Comment)
