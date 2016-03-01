from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(alertRecord)
admin.site.register(alertReport)
admin.site.register(monitorItems)
admin.site.register(alertUsersGroups)