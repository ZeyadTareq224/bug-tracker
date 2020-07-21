from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
	path('projects/dashboard/', views.project_dashboard, name='project_dashboard'),
	path('ticket/dashboard/', views.ticket_dashboard, name='ticket_dashboard'),
	path('dev_dashboard/', views.dev_dashboard, name='dev_dashboard'),
	path('pm_dashboard/', views.pm_dashboard, name='pm_dashboard'),
	path('sub_dashboard/', views.sub_dashboard, name='sub_dashboard'),
	path('demo_selection/', views.demo_selection, name='demo_selection'),

	#authentication
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),

	#registration
	path('register/', views.registeration, name='register'),


	path('user/update/<str:pk>', views.update_user, name='update_user'),
	path('user/delete/<str:pk>', views.delete_user, name='delete_user'),

	path('user/profile/', views.profile, name='profile'),
	path('user/account_settings/', views.account_settings, name='account_settings'),

]