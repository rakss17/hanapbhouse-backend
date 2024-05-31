from django.contrib import admin
from . import models

admin.site.register(models.Property)
admin.site.register(models.Address)
admin.site.register(models.Room)

