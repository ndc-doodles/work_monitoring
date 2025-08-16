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
    path('teamlead/index/', views.teamlead_index, name='teamlead_index'),
    path('submit-report/', views.submit_report, name='submit_report'),
    path('teamlead_assign_project/', views.teamlead_assign_project, name='teamlead_assign_project'),
    path('teammember_assigned_projects/', views.teammember_assigned_projects, name='teammember_assigned_projects'),
    path('ajax/get-team-members/', views.get_team_members, name='get_team_members'),

    path('teamlead/project/edit/<int:project_id>/', views.edit_assigned_project, name='edit_assigned_project'),
    path('teamlead/project/delete/<int:project_id>/',views. delete_assigned_project, name='delete_assigned_project'),
    path('teamlead_reports/', views.teamlead_reports, name='teamlead_reports'),
    path('all_reports_view/', views.all_reports_view, name='all_reports'),





    path('teammember_login/', views.teammember_login, name='teammember_login'),
    path('teammember_index/', views.teammember_index, name='teammember_index'),
]
