from django.contrib import admin
from apps.projects.models import *

admin.site.register(Project)
admin.site.register(ProjectCategory)
admin.site.register(ActivityCategory)
admin.site.register(Activity)