from django.contrib import admin
from . models import *

admin.site.register(Department)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Announcement)
# admin.site.register(MorningReport)
# admin.site.register(EveningReport)
admin.site.register(ProjectAssign)


