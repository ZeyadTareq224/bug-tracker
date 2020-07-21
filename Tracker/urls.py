from django.urls import path
from . import views

urlpatterns = [
	path('create_project/', views.create_project, name='create_project'),
	path('update_project/<str:pk>/', views.update_project, name='update_project'),
	path('delete_project/<str:pk>', views.delete_project, name='delete_project'),
	path('project_details/<str:pk>', views.project_details, name='project_details'),
	path('ticket_details/<str:pk>', views.ticket_details, name='ticket_details'),
	path('ticket_create/', views.ticket_create, name='ticket_create'),
	path('ticket_update/<str:pk>', views.ticket_update, name='ticket_update'),
	path('ticket_delete/<str:pk>', views.delete_ticket, name='ticket_delete'),
	path('ticket_status_update/<str:pk>', views.ticket_status_update, name='ticket_status_update'),

	#ticket comments
	path('update_comment/<str:pk>', views.update_comment, name='update_comment'),
	path('delete_comment/<str:pk>', views.delete_comment, name='delete_comment'),

	#project comments
	path('update_p_comment/<str:pk>', views.update_project_comment, name='update_p_comment'),
	path('delete_p_comment/<str:pk>', views.delete_project_comment, name='delete_p_comment'),

	#developers re-assignment
	path('re_assign/<str:pk>', views.re_assign_devs, name='re_assign')
]