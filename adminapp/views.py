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
from django.http import JsonResponse





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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            teamlead = User.objects.get(email=email, password=password, role="Team Lead")
            request.session["user_id"] = teamlead.id   # 👈 Fixed key
            print("✅ Login success:", teamlead.id)  
            return redirect("teamlead_index")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("teamlead_login")

    return render(request, "teamlead_login.html")


def teamlead_index(request):
    user_id = request.session.get('user_id')  # 👈 Consistent key
    if not user_id:
        return redirect('teamlead_login')

    try:
        user = User.objects.get(id=user_id, role='Team Lead')
    except User.DoesNotExist:
        return redirect('teamlead_login')

    team_members = User.objects.filter(
        team=user.team,
        role='Team Member'
    )

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
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email, password=password, role="Team Member")
            # Store the user ID in session
            request.session['teammember_id'] = user.id
            return redirect('teammember_assigned_projects')  # Redirect after login
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect('teammember_login')

    return render(request, "teammember_login.html")

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
    # Check if teamlead is logged in
    teamlead_id = request.session.get('teamlead_id')
    if not teamlead_id:
        return redirect('teamlead_login')

    teamlead = User.objects.get(id=teamlead_id)
    team = teamlead.team
    departments = Department.objects.all()  # For department dropdown

    # Handle form submission
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_type = request.POST.get('project_type')
        category = request.POST.get('category')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        additional_notes = request.POST.get('additional_notes')
        assigned_to_id = request.POST.get('assigned_to')
        department_id = request.POST.get('department')

        # Get department and assigned user objects
        department = Department.objects.get(id=department_id)
        assigned_to = User.objects.get(id=assigned_to_id)

        # Create the assigned project
        AssignedProject.objects.create(
            project_name=project_name,
            project_type=project_type,
            category=category,
            description=description,
            deadline=deadline,
            additional_notes=additional_notes,
            department=department,
            team=team,
            assigned_by=teamlead,
            assigned_to=assigned_to,
        )

        return redirect('teamlead_assign_project')  # Reload page to see new project

    # Fetch all projects assigned by this teamlead for this team
    assigned_projects = AssignedProject.objects.filter(
        assigned_by=teamlead,
        team=team
    ).order_by('-date_assigned')  # latest projects first

    # Render template with form data and assigned projects
    context = {
        'team': team,
        'departments': departments,
        'assigned_projects': assigned_projects,
    }

    return render(request, 'teamlead_assign_project.html', context)

def get_team_members(request):
    teamlead_id = request.session.get('teamlead_id')
    if not teamlead_id:
        return JsonResponse({"error": "Not logged in"}, status=403)

    teamlead = User.objects.get(id=teamlead_id)
    team = teamlead.team
    department_id = request.GET.get('department_id')

    if not department_id:
        return JsonResponse({"members": []})

    members = User.objects.filter(
        team=team,
        department_id=department_id,
        role="Team Member"
    ).values("id", "name")

    return JsonResponse({"members": list(members)})
   


def teammember_assigned_projects(request):
    # Get logged-in Team Member ID from session
    teammember_id = request.session.get('teammember_id')
    if not teammember_id:
        return redirect('teammember_login')

    try:
        user = User.objects.get(id=teammember_id, role='Team Member')
    except User.DoesNotExist:
        # If the user doesn't exist or role mismatch, force login
        return redirect('teammember_login')

    # Fetch projects assigned to this team member
    projects = AssignedProject.objects.filter(
        assigned_to=user
    ).order_by('-date_assigned')  # latest first

    return render(request, 'teammember_assignedprojects.html', {
        'projects': projects
    })




def edit_assigned_project(request, project_id):
    project = get_object_or_404(AssignedProject, id=project_id)
    teamlead_id = request.session.get('teamlead_id')
    if project.assigned_by.id != teamlead_id:
        return redirect('teamlead_assign_project')

    if request.method == 'POST':
        project.project_name = request.POST.get('project_name')
        project.project_type = request.POST.get('project_type')
        project.category = request.POST.get('category')
        project.description = request.POST.get('description')
        project.deadline = request.POST.get('deadline')
        project.additional_notes = request.POST.get('additional_notes')
        assigned_to_id = request.POST.get('assigned_to')
        project.assigned_to = User.objects.get(id=assigned_to_id)
        project.save()
        return redirect('teamlead_assign_project')

    departments = Department.objects.all()
    team = project.team
    return render(request, 'edit_assigned_project.html', {
        'project': project,
        'departments': departments,
        'team': team,
    })


def delete_assigned_project(request, project_id):
    project = get_object_or_404(AssignedProject, id=project_id)
    teamlead_id = request.session.get('teamlead_id')
    if project.assigned_by.id == teamlead_id:
        project.delete()
    return redirect('teamlead_assign_project')