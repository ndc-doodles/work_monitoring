from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Report
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import localdate
from datetime import date




def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  # change this to your main page
        else:
            messages.error(request, "Invalid credentials or not a superuser")
    return render(request, 'admin_login.html')





def admin_dashboard(request):
    if request.method == 'POST':
        # Add Department
        if 'add_dept' in request.POST:
            name = request.POST.get('dept_name')
            if name:
                Department.objects.create(name=name)
            return redirect('admin_dashboard')

        # Delete Department
        elif 'delete_dept' in request.POST:
            dept_id = request.POST.get('delete_dept')
            Department.objects.filter(id=dept_id).delete()
            return redirect('admin_dashboard')

        # Add Team
        elif 'add_team' in request.POST:
            name = request.POST.get('team_name')
            if name:
                Team.objects.create(name=name)
            return redirect('admin_dashboard')

        # Delete Team
        elif 'delete_team' in request.POST:
            team_id = request.POST.get('delete_team')
            Team.objects.filter(id=team_id).delete()
            return redirect('admin_dashboard')

    # Dashboard counts and lists
    total_users = User.objects.count()
    online_users = User.objects.filter(status='Online').count()
    idle_users = User.objects.filter(status='Idle').count()
    offline_users = User.objects.filter(status='Offline').count()
    departments = Department.objects.all()
    teams = Team.objects.all()

    return render(request, 'admin_dashboard.html', {
        'total_users': total_users,
        'online_users': online_users,
        'idle_users': idle_users,
        'offline_users': offline_users,
        'departments': departments,
        'teams': teams
    })

def admin_user_management(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        department_id = request.POST.get('department')
        team_id = request.POST.get('team')
        role = request.POST.get('role')

        if all([name, email, password, department_id, team_id, role]):
            department = Department.objects.get(id=department_id)
            team = Team.objects.get(id=team_id)
            User.objects.create(
                name=name,
                email=email,
                password=password,
                department=department,
                team=team,
                role=role
            )
        return redirect('admin_user_management')

    users = User.objects.all()
    departments = Department.objects.all()
    teams = Team.objects.all()
    return render(request, 'admin_user_management.html', {
        'users': users,
        'departments': departments,
        'teams': teams
    })


def update_user(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        role = request.POST.get('role')
        department_id = request.POST.get('department')
        team_id = request.POST.get('team')

        user = get_object_or_404(User, id=user_id)
        user.name = name
        user.email = email
        user.role = role
        user.department_id = department_id
        user.team_id = team_id
        user.save()
    return redirect('admin_user_management')



def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_user_management')

def admin_work_monitor(request):
    departments = Department.objects.all()
    teams = Team.objects.all()

    selected_dept = request.GET.get('department')
    selected_team = request.GET.get('team')

    users = User.objects.all()
    if selected_dept:
        users = users.filter(department_id=selected_dept)
    if selected_team:
        users = users.filter(team_id=selected_team)

    return render(request, 'admin_work_monitor.html', {
        'users': users,
        'departments': departments,
        'teams': teams,
        'selected_dept': selected_dept,
        'selected_team': selected_team,
    })

def admin_export_excel(request):
    users = User.objects.all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Work Monitoring"

    sheet.append(["Name", "Email", "Department", "Team", "Role", "Current Work", "Excel Link"])

    for user in users:
        try:
            link = user.profile.work_link
        except:
            link = ''
        sheet.append([
            user.get_full_name(),
            user.email,
            user.department.name if user.department else '',
            user.team.name if user.team else '',
            user.role,
            user.profile.current_work if hasattr(user.profile, 'current_work') else '',
            link
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=admin_work_monitor.xlsx'
    workbook.save(response)
    return response


def admin_logout(request):
    logout(request)
    return redirect('login') 




def welcome(request):
    return render(request, 'welcome.html')

def teamlead_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email, password=password, role='Team Lead')
            request.session['user_id'] = user.id  # ✅ store team lead's ID in session
            return redirect('teamlead_reports')
        except User.DoesNotExist:
            return render(request, 'teamlead_login.html', {'error': 'Invalid credentials'})

    return render(request, 'teamlead_login.html')

def teamlead_index(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('teamlead_login')

    try:
        user = User.objects.get(id=user_id, role='Team Lead')
    except User.DoesNotExist:
        return redirect('teamlead_login')

    # Now fetch team members of the same team (excluding the Team Lead themselves)
    team_members = User.objects.filter(
        team=user.team,
        role='Team Member'
    )

    # Count unique projects (non-empty) from those team members
    total_projects = (
        team_members.exclude(current_project="")
                    .values('current_project')
                    .distinct()
                    .count()
    )

    context = {
        'teamlead': user,
        'team_members': team_members,
        'total_team_members': team_members.count(),
        'total_projects': total_projects,
    }

    return render(request, 'teamlead_index.html', context)  

@csrf_exempt
def submit_report(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')  # or appropriate redirect

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect('login')

        report_type = request.POST.get('report_type')  # ✅ correct key name
        content = request.POST.get('content')

        # ✅ Assign user's team explicitly
        Report.objects.create(
            user=user,
            team=user.team,  # ✅ critical line
            type=report_type,
            content=content
        )

        return redirect('teammember_index')  # or wherever

    return redirect('teammember_index')




def teamlead_reports(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('teamlead_login')

    try:
        team_lead = User.objects.get(id=user_id, role='Team Lead')
    except User.DoesNotExist:
        return redirect('teamlead_login')

    today = date.today()

    morning_reports = Report.objects.filter(
        team=team_lead.team,
        type='morning',
        submitted_at__date=today
    ).select_related('user', 'team', 'user__department')

    evening_reports = Report.objects.filter(
        team=team_lead.team,
        type='evening',
        submitted_at__date=today
    ).select_related('user', 'team', 'user__department')

    return render(request, 'teamlead_reports.html', {
        'morning_reports': morning_reports,
        'evening_reports': evening_reports,
    })





def teammember_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, password=password, role='Team Member')
            request.session['user_id'] = user.id
            print("✅ Team Member Logged In:", user.name)
            return redirect('teammember_index')  # This should work
        except User.DoesNotExist:
            error = "Invalid credentials or not a Team Member"
            print("❌ Login failed")
            return render(request, 'teammember_login.html', {'error': error})

    return render(request, 'teammember_login.html')

def teammember_index(request):
    user_id = request.session.get('user_id')
    print("🔍 Session user_id:", user_id)
    if not user_id:
        return redirect('teammember_login')

    try:
        user = User.objects.get(id=user_id, role='Team Member')
    except User.DoesNotExist:
        return redirect('teammember_login')

    same_team_members = User.objects.filter(team=user.team, role='Team Member').exclude(id=user.id)

    today = localdate()  # gets current date in local timezone

    morning_report = Report.objects.filter(user=user, type='morning', submitted_at__date=today).first()
    evening_report = Report.objects.filter(user=user, type='evening', submitted_at__date=today).first()

    context = {
        'teammember': user,
        'same_team_members': same_team_members,
        'morning_report': morning_report,
        'evening_report': evening_report,
    }
    return render(request, 'teammember_index.html', context)


def all_reports_view(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Ensure only logged-in users can access

    try:
        current_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    if current_user.role != 'Team Lead':
        return redirect('login')  # Or show an access denied message

    # Get all morning and evening reports for users in this team
    team_members = User.objects.filter(team=current_user.team, role='Team Member')

    morning_reports = Report.objects.filter(user__in=team_members, type='morning').select_related('user', 'user__team', 'user__department').order_by('-submitted_at')
    evening_reports = Report.objects.filter(user__in=team_members, type='evening').select_related('user', 'user__team', 'user__department').order_by('-submitted_at')

    return render(request, 'all_reports.html', {
        'morning_reports': morning_reports,
        'evening_reports': evening_reports
    })


def teamlead_assign_project(request):
    departments = Department.objects.all()
    team_members = User.objects.all()

    if request.method == 'POST':
        # Handle form submission and save project assignment
        # Extract data from request.POST here
        pass

    return render(request, 'teamlead_assign_project.html', {
        'departments': departments,
        'team_members': team_members,
    })
  
    
def team_member_projects_view(request):
    projects = AssignedProject.objects.filter(assigned_to=request.user).order_by('-date_assigned')
    return render(request, 'team_member_projects.html', {'projects': projects})
