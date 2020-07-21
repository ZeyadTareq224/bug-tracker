from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.png', upload_to='profile_pics')
	phone = models.CharField(max_length=15, null=True)

	def __str__(self):
		return self.user.username

class ProjectManager(models.Model):
	project_manager = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	is_developer = models.BooleanField(default=False)
	is_project_manager = models.BooleanField(default=True)
	is_submitter = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	def __str__(self):
		return self.project_manager.username


class Developer(models.Model):
	developer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	is_developer = models.BooleanField(default=True)
	is_project_manager = models.BooleanField(default=False)
	is_submitter = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	def __str__(self):
		return self.developer.username


class Submitter(models.Model):
	submitter = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	is_submitter = models.BooleanField(default=True)
	is_developer = models.BooleanField(default=False)
	is_project_manager = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	def __str__(self):
		return self.submitter.username


class Admin(models.Model):
	admin = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	is_developer = models.BooleanField(default=False)
	is_project_manager = models.BooleanField(default=False)
	is_submitter = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=True)

	def __str__(self):
		return self.admin.username
