from django.contrib import admin
from .models import Ticket, Project, TicketComment, ProjectComment

admin.site.register(Ticket)
admin.site.register(Project)
admin.site.register(TicketComment)
admin.site.register(ProjectComment)
