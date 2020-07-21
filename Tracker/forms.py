from django import forms
from .models import Project, Ticket, TicketComment, ProjectComment

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = '__all__'
		exclude = ['created_at', 'updated_at', 'project_manager']

class TicketForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = '__all__'
		exclude = ['created_at', 'updated_at', 'submitters']

class TicketCommentForm(forms.ModelForm):
	class Meta:
		model = TicketComment
		fields = ['comment']

class ProjectCommentForm(forms.ModelForm):
	class Meta:
		model = ProjectComment
		fields = ['comment']		

class UpdateTicketStatusForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['status']

class ReAssignDevsForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['assigned_devs']		