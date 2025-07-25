from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_user_management/', views.admin_user_management, name='admin_user_management'),

    path('update_user/', views.update_user, name='update_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_work_monitor/', views.admin_work_monitor, name='admin_work_monitor'),
    path('admin_export_excel/', views.admin_export_excel, name='admin_export_excel'),
    path('admin_logout/', LogoutView.as_view(next_page='/admin_login/'), name='admin_logout'),



    path('', views.welcome, name='welcome'),
    path('teamlead_login/', views.teamlead_login, name='teamlead_login'),
    path('teamlead_index/', views.teamlead_index, name='teamlead_index'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('assign_project_view/', views.assign_project_view, name='assign_project_view'),
    path('team_member_projects_view/', views.team_member_projects_view, name='team_member_projects_view'),

    path('teamlead_reports/', views.teamlead_reports, name='teamlead_reports'),
    path('all_reports_view/', views.all_reports_view, name='all_reports'),





    path('teammember_login/', views.teammember_login, name='teammember_login'),
    path('teammember_index/', views.teammember_index, name='teammember_index'),
]
