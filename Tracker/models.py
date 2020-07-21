from django.db import models
from django.contrib.auth.models import User
from users.models import Developer, Submitter, ProjectManager
import datetime

class Project(models.Model):
	title = models.CharField(max_length=50, null=True)
	description = models.TextField(max_length=5000, null=True)
	project_manager = models.ForeignKey(ProjectManager, on_delete=models.SET_NULL, null=True)
	assigned_devs = models.ManyToManyField(Developer)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.title


class Ticket(models.Model):
	STATUS = (('Open', 'Open'), ('Closed', 'Closed'))	
	PRIORITY = (('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'))
	TICKET_TYPE = (('Bug', 'Bug'), ('Error', 'Error'), ('feature_request', 'Feature Request'))
	developers = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True)
	submitters = models.ForeignKey(Submitter, on_delete=models.SET_NULL, null=True)
	title = models.CharField(max_length=50, null=True)
	description = models.TextField(max_length=5000, null=True)
	status = models.CharField(max_length=6, choices=STATUS, null=True)
	priority = models.CharField(max_length=6, choices=PRIORITY, null=True)
	ticket_type = models.CharField(max_length=15, choices=TICKET_TYPE, null=True)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class TicketComment(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField(max_length=10000)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.commenter.username


class ProjectComment(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField(max_length=10000)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.commenter.username

