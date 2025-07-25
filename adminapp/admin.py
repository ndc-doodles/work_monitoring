from django.contrib import admin
from adminapp import models

admin.site.register(models.Department)
admin.site.register(models.Team)
admin.site.register(models.User)
admin.site.register(models.Report)

