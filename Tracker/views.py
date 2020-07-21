from django.shortcuts import render, redirect
from .forms import ProjectForm, TicketForm, TicketCommentForm, UpdateTicketStatusForm, ProjectCommentForm, ReAssignDevsForm
from .models import Project, Ticket, TicketComment, ProjectComment
from django.contrib import messages
from users.models import ProjectManager
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users


@allowed_users(['admin', 'project_manager'])
@login_required(login_url='login')
def create_project(request):
	user = request.user
	pm = ProjectManager.objects.get(project_manager = user)
	form = ProjectForm()
	if request.method == "POST":
		form = ProjectForm(request.POST)
		if form.is_valid():
			form.instance.project_manager = pm
			form.save()
			messages.success(request, 'Project created successfully.')
			return redirect('create_project')

	context = {'form': form}
	return render(request, 'Tracker/project_form.html', context)




@allowed_users(['admin', 'project_manager'])
@login_required(login_url='login')
def update_project(request, pk):
	project = Project.objects.get(id=pk)
	form = ProjectForm(instance=project)
	if request.method == "POST":
		form = ProjectForm(data=request.POST, instance=project)
		if form.is_valid():
			form.save()
			messages.success(request, 'submitted successfully.')
			if request.user.admin:
				return redirect('project_dashboard')
			elif request.user.groups.get().name == "project_manager":
				return redirect('pm_dashboard')	

	context = {'form': form}
	return render(request, 'Tracker/project_form.html', context)




@allowed_users(['admin', 'project_manager'])
@login_required(login_url='login')
def delete_project(request, pk):
	project = Project.objects.get(id=pk)
	if request.method == "POST":
		project.delete()
		messages.success(request, 'project deleted successfully.')
		if request.user.admin:
			return redirect('project_dashboard')
		elif request.user.groups.get().name == "project_manager":
			return redirect('pm_dashboard')
	context = {'project': project}
	return render(request, 'Tracker/delete_project.html', context)	





@login_required(login_url='login')
def project_details(request, pk):
	project = Project.objects.get(id=pk)
	project_tickets = Ticket.objects.filter(project=project)
	project_comments = ProjectComment.objects.filter(project=project).order_by('-created_at')
	form = ProjectCommentForm()
	if request.method == "POST":
		form = ProjectCommentForm(request.POST)
		if form.is_valid():
			form.instance.commenter = request.user
			form.instance.project = project
			form.save()
			messages.success(request, 'Comment submitted successfully.')
			return redirect('project_details', pk)

	context = {'project': project, 'project_tickets': project_tickets, 'form': form, 'project_comments': project_comments}
	return render(request, 'Tracker/project_details.html', context)






@login_required(login_url='login')
def ticket_details(request, pk):
	ticket = Ticket.objects.get(id=pk)
	ticket_comments = TicketComment.objects.filter(ticket=ticket).order_by('-created_at')
	form = TicketCommentForm()
	if request.method == "POST":
		form = TicketCommentForm(request.POST)
		if form.is_valid():
			form.instance.commenter = request.user
			form.instance.ticket = ticket
			form.save()
			messages.success(request, 'Comment submitted successfully.')
			return redirect('ticket_details', pk)

	context = {'ticket': ticket, 'ticket_comments': ticket_comments, 'form':form}
	return render(request, 'Tracker/ticket_details.html', context)




@allowed_users(['admin', 'submitter'])
@login_required(login_url='login')
def ticket_create(request):
	form = TicketForm()
	if request.method == "POST":
		form = TicketForm(request.POST)
		if form.is_valid():
			form.instance.submitters = request.user.submitter
			form.save()
			messages.success(request, 'Ticket created successfully.')
			if request.user.groups.get().name == "admin":
				return redirect('admin_dashboard')
			elif request.user.groups.get().name == "submitter":
				return redirect('sub_dashboard')	
	context = {'form': form}
	return render(request, 'Tracker/ticket_form.html', context)




@allowed_users(['admin', 'project_manager', 'submitter'])
@login_required(login_url='login')
def ticket_update(request, pk):
	ticket = Ticket.objects.get(id=pk)
	form = TicketForm(instance=ticket)
	if request.method == "POST":
		form = TicketForm(data=request.POST, instance=ticket)
		if form.is_valid():
			form.save()
			messages.success(request, 'Ticket updated successfully.')
			if request.user.groups.get().name == 'admin':
				return redirect('ticket_dashboard')
			elif request.user.groups.get().name == 'submitter':
				return redirect('ticket_details', ticket.id)
				
	context = {'form': form, 'ticket': ticket}
	return render(request, 'Tracker/ticket_form.html', context)




@allowed_users(['admin', 'project_manager', 'submitter'])
@login_required(login_url='login')
def delete_ticket(request, pk):
	ticket = Ticket.objects.get(id=pk)
	ticket_project_id = ticket.project.id
	if request.method == "POST":
		ticket.delete()
		messages.success(request, "Ticket deleted successfully.")
		if request.user.groups.get().name == 'project_manager':
			return redirect('project_details', ticket_project_id)
		elif request.user.groups.get().name == 'admin':
			return redirect('ticket_dashboard')	
		elif request.user.groups.get().name == 'submitter':
			return redirect('sub_dashboard')
		

	context = {'ticket': ticket}
	return render(request, 'Tracker/delete_ticket.html', context)	





@allowed_users(['admin', 'developer'])
@login_required(login_url='login')
def ticket_status_update(request, pk):
	ticket = Ticket.objects.get(id=pk)
	form = UpdateTicketStatusForm(instance=ticket)
	if request.method == "POST":
		form = UpdateTicketStatusForm(request.POST, instance=ticket)
		if form.is_valid():
			form.save()
			messages.success(request, 'Ticket updated successfully.')
			return redirect('dev_dashboard')

	context = {'form': form, 'ticket': ticket}
	return render(request, 'Tracker/ticket_status_update.html', context)		





@login_required(login_url='login')
def update_comment(request, pk):
	comment = TicketComment.objects.get(id=pk)

	form = TicketCommentForm(instance=comment)
	if request.method == "POST":
		form = TicketCommentForm(request.POST, instance=comment)
		if form.is_valid():
			form.save()
			messages.success(request, 'comment updated successfully.')
			return redirect('ticket_details', comment.ticket.id)

	context = {'form': form, 'comment': comment}		
	return render(request, 'Tracker/comment_form.html', context)






@login_required(login_url='login')
def delete_comment(request, pk):
	comment = TicketComment.objects.get(id=pk)

	if request.method == "POST":
		comment.delete()
		messages.success(request, 'Comment deleted successfully')
		return redirect('ticket_details', comment.ticket.id)
	context = {'comment': comment}
	return render(request, 'Tracker/delete_comment.html', context)





@login_required(login_url='login')
def update_project_comment(request, pk):
	comment = ProjectComment.objects.get(id=pk)
	form = ProjectCommentForm(instance=comment)
	if request.method == "POST":
		form = ProjectCommentForm(request.POST, instance=comment)
		if form.is_valid():
			form.save()
			messages.success(request, 'Comment updated successfully.')
			return redirect('project_details', comment.project.id)
	context = {'form': form, 'comment': comment}		
	return render(request, 'Tracker/project_comment_form.html', context)






@login_required(login_url='login')
def delete_project_comment(request, pk):
	comment = ProjectComment.objects.get(id=pk)
	if request.method == "POST":
		comment.delete()
		messages.success(request, 'Your comment deleted successfully.')
		return redirect('project_details', comment.project.id)
	context = {'comment': comment}
	return render(request, 'Tracker/delete_project_comment.html', context)





@allowed_users(['admin', 'project_manager'])
@login_required(login_url='login')
def re_assign_devs(request, pk):
	project = Project.objects.get(id=pk)
	form = 	ReAssignDevsForm(instance=project)
	if request.method == "POST":
		form = ReAssignDevsForm(request.POST, instance=project)
		if form.is_valid():
			messages.success(request, 'Developers Re-Assigned successfully.')
			form.save()
			return redirect('project_details', pk)

	context = {'form': form, 'project': project}
	return render(request, 'Tracker/re_assign_form.html', context)		
