from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group,User
from .forms import RegistrationForm, UserUpdateForm, ProfileImageForm, AccountSettingsForm, AccountPrivacyForm
from .models import Profile, ProjectManager, Submitter
from Tracker.models import Project, Ticket
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
@allowed_users(['admin'])
def admin_dashboard(request):
	projects = Project.objects.all()



	users = User.objects.all()
	total_users = users.count()
	total_admins = Group.objects.get(name="admin").user_set.all().count()
	total_developers = Group.objects.get(name="developer").user_set.all().count()
	total_project_managers = Group.objects.get(name="project_manager").user_set.all().count()
	total_submitters = Group.objects.get(name="submitter").user_set.all().count()

	admins_precentage =(total_admins*100)/total_users
	developers_precentage = (total_developers*100)/total_users
	admins_project_managers = (total_project_managers*100)/total_users
	admins_submitters = (total_submitters*100)/total_users

	context = {
	'users': users,
	'total_admins': total_admins,
	'total_developers': total_developers,
	'total_project_managers': total_project_managers,
	'total_submitters': total_submitters,
	'admins_precentage': admins_precentage,
	'developers_precentage': developers_precentage,
	'admins_project_managers': admins_project_managers,
	'admins_submitters': admins_submitters,
	'projects': projects
	}
	return render(request, 'users/admin_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['developer'])
def dev_dashboard(request):
	dev = request.user.developer
	dev_tickets = Ticket.objects.filter(developers=dev)
	dev_open_tickets = dev_tickets.filter(status='Open')
	dev_closed_tickets  = dev_tickets.filter(status='Closed')


	dev_projects = Project.objects.filter(assigned_devs = dev)

	context = {
	'dev': dev,
	'dev_tickets': dev_tickets,
	'dev_open_tickets': dev_open_tickets,
	'dev_closed_tickets': dev_closed_tickets,
	'dev_projects': dev_projects,
	}
	return render(request, 'users/devs_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['project_manager'])
def pm_dashboard(request):
	user = request.user
	pm = ProjectManager.objects.get(project_manager = user)
	projects = Project.objects.filter(project_manager=pm)


	context = {'projects': projects}
	return render(request, 'users/pm_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['submitter'])
def sub_dashboard(request):
	sub = request.user.submitter
	sub_tickets = Ticket.objects.filter(submitters=sub)
	total_open_tickets = sub_tickets.filter(status='Open').count()
	total_closed_tickets = sub_tickets.filter(status = 'Closed').count()

	context = {'sub_tickets': sub_tickets, 'total_open_tickets': total_open_tickets, 'total_closed_tickets': total_closed_tickets}
	return render(request, 'users/sub_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
def project_dashboard(request):
	projects = Project.objects.all()
	pms = ProjectManager.objects.all()
	context = {'projects': projects, 'pms': pms}
	return render(request, 'users/project_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
def ticket_dashboard(request):
	tickets = Ticket.objects.all()
	subs = Submitter.objects.all()
	context = {'tickets': tickets, 'subs': subs}
	return render(request, 'users/ticket_dashboard.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
def update_user(request, pk):
	user = User.objects.get(id=pk)
	form = UserUpdateForm(instance=user)
	if request.method == "POST":
		form = UserUpdateForm(instance=user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'User data updated successfully.')
			return redirect('admin_dashboard')
	context = {'form': form}
	return render(request, 'users/user_update_form.html', context)	


@login_required(login_url='login')
@allowed_users(['admin'])
def delete_user(request, pk):
	user = User.objects.get(id=pk)
	if request.method == "POST":
		user.delete()
		return redirect('admin_dashboard')

	context = {'user': user}
	return render(request, 'users/delete_user.html', context)	

@login_required(login_url='login')
def profile(request):
	profile = Profile.objects.get(user=request.user)
	form = ProfileImageForm(instance=profile)
	if request.method == "POST":
		form = ProfileImageForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile')
	context = {'form': form}
	return render(request, 'users/profile.html', context)

@login_required(login_url='login')
def account_settings(request):
	user = request.user
	profile = request.user.profile
	u_form = AccountPrivacyForm(instance=user)
	p_form = AccountSettingsForm(instance=profile)
	if request.method == "POST":
		u_form = AccountPrivacyForm(request.POST, instance=user)
		p_form = AccountSettingsForm(request.POST, instance=profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Account settings updated successfully.')
			return redirect('account_settings')

	context = {'u_form': u_form, 'p_form': p_form}		
	return render(request, 'users/account_settings.html', context)		

def home(request):

	context = {}
	return render(request, 'users/home.html', context)

def demo_selection(request):

	context = {}
	return render(request, 'users/users_login.html', context)


def login_page(request):
	admin_users = list(Group.objects.get(name="admin").user_set.all())
	dev_users = list(Group.objects.get(name="developer").user_set.all())
	pm_users = list(Group.objects.get(name="project_manager").user_set.all())
	sub_users = list(Group.objects.get(name="submitter").user_set.all())

	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		if user is not None:
			if user in admin_users:
				login(request, user)
				return redirect('admin_dashboard')
			elif user in dev_users:
				login(request, user)
				return redirect('dev_dashboard')
			elif user in pm_users:
				login(request, user)
				return redirect('pm_dashboard')
			elif user in sub_users:
				login(request, user)
				return redirect('sub_dashboard')
		else:
			messages.info(request, 'Username or Password is incorrect.')
	return render(request, 'users/login.html')

@login_required(login_url='login')
def logout_page(request):
	logout(request)
	messages.success(request, 'you have logged out successfully')
	return redirect('login')

def registeration(request):
	form = RegistrationForm()
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Your account has been created, you need to wait for admin confirmation.')
			return redirect('login')
	context = {'form': form}
	return render(request, 'users/registeration.html', context)

