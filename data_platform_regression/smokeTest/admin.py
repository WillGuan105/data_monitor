from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Modules)
admin.site.register(Interface)
admin.site.register(runResult)