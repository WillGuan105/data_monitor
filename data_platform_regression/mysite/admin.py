from django.contrib import admin
from .models import *
from alertStrategy.models import *

admin.site.register(Report)
admin.site.register(Graph)
admin.site.register(ReportResult)
admin.site.register(GraphResult)
