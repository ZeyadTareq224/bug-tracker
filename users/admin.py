from django.contrib import admin
from .models import ProjectManager, Developer, Submitter, Admin, Profile

admin.site.register(ProjectManager)
admin.site.register(Developer)
admin.site.register(Submitter)
admin.site.register(Admin)
admin.site.register(Profile)

# Register your models here.
