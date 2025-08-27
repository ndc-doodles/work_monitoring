from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  
from .models import *
from datetime import datetime

def index(request):
    return render(request,'index.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')  
        else:
            messages.error(request, "Invalid credentials or not a superuser")
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    if request.method == "POST":
        if "add_department" in request.POST:
            name = request.POST.get("department_name")
            if name:
                Department.objects.create(name=name)
                return redirect('admin_dashboard')

        elif "add_team" in request.POST:
            name = request.POST.get("team_name")
            if name:
                Team.objects.create(name=name)
                return redirect('admin_dashboard')

    departments = Department.objects.all()
    teams = Team.objects.all()
    return render(request, "admin_dashboard.html", {"departments": departments, "teams": teams})






def delete_department(request, pk):
    dept = get_object_or_404(Department, pk=pk)
    dept.delete()
    return redirect('admin_dashboard')

def delete_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    return redirect('admin_dashboard')



def admin_usermanagement(request):

    users = User.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        employee_id = request.POST.get("employee_id")   # ✅ Added
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        department = request.POST.get("department")
        team = request.POST.get("team")                 # ✅ Added
        job_Position = request.POST.get("job_Position")
        designation = request.POST.get("designation")
        work_location = request.POST.get("work_location")  # ✅ Added
        joining_date = request.POST.get("joining_date")    # ✅ Added (but careful, model has auto_now_add=True)
        username = request.POST.get("username")
        password = request.POST.get("password")  
        status = request.POST.get("status")             # ✅ Added
        image = request.FILES.get("profile_image")

        # ✅ Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ Username already exists. Please choose another one.")
            return redirect("admin_usermanagement")

        # ✅ Create only if username is unique
        User.objects.create(
            name=name,
            employee_id=employee_id,
            email=email,
            phone=phone,
            department=department,
            team=team,
            job_Position=job_Position,
            designation=designation,
            work_location=work_location,
            # ⚠️ joining_date is auto_now_add=True → You don’t need to pass it,
            # remove from model or make it models.DateField() if you want custom input
            username=username,
            password=password,  
            status=status,
            profile_image=image
        )
        messages.success(request, "✅ User created successfully!")
        return redirect("admin_usermanagement")

    return render(request, "admin_usermanagement.html", {"users": users})




def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect('admin_usermanagement') 


def edit_user(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        user = get_object_or_404(User, id=user_id)

        user.employee_id = request.POST.get("edit_emp_id")
        user.name = request.POST.get("edit_name")
        user.email = request.POST.get("edit_email")
        user.phone = request.POST.get("edit_phone")
        user.department = request.POST.get("edit_department")
        user.team = request.POST.get("edit_team")
        user.job_Position = request.POST.get("edit_job_position")

        user.designation = request.POST.get("edit_designation")
        user.work_location = request.POST.get("edit_work_location")
        user.username = request.POST.get("edit_username")
        user.status = request.POST.get("edit_status")

        # Handle joining_date safely
        joining_date = request.POST.get("edit_joining_date")
        if joining_date:  # if not empty
            try:
                user.joining_date = datetime.strptime(joining_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format! Please use YYYY-MM-DD.")
                return redirect("admin_usermanagement")
        else:
            user.joining_date = None  # allow empty date

        if request.FILES.get("edit_profile_upload"):
            user.profile_image = request.FILES.get("edit_profile_upload")

        user.save()
        messages.success(request, "User updated successfully!")
        return redirect('admin_usermanagement')

    return redirect('admin_usermanagement')







def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        position = request.POST.get("position")

        try:
            user = User.objects.get(username=username)
            
            if user.password == password:
                db_position = user.job_Position.lower().replace(" ", "_")
                if db_position == position:
                    request.session['user_id'] = user.id
                    if position == "team_lead":
                        return redirect('teamlead_dashboard')
                    else:
                        return redirect('teammember_dashboard')
                else:
                    messages.error(request, "Invalid position for this user")
            else:
                messages.error(request, "Invalid username or password")
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, 'user_login.html')


def teamlead_dashboard(request):
    team_lead = User.objects.get(id=request.session['user_id'])  
    team_name = team_lead.team  

    if request.method == "POST":
        message = request.POST.get("message")
        if message.strip():
            Announcement.objects.create(
                title="Announcement",
                message=message,
                created_by=team_lead,
                created_at=timezone.now()
            )
        return redirect('teamlead_dashboard')

    # ✅ Get all team members EXCEPT the logged-in team lead
    team_members = User.objects.filter(team=team_name).exclude(id=team_lead.id)

    # ✅ Count team members only (not including team lead)
    total_users = team_members.count()
    active_members = team_members.filter(status="active").count()
    inactive_members = team_members.filter(status="inactive").count()

    # ✅ Show announcements from last 12 hrs
    cutoff = timezone.now() - timedelta(hours=12)
    announcements = Announcement.objects.filter(
        created_by=team_lead,
        created_at__gte=cutoff
    ).order_by('-created_at')

    return render(request, 'teamlead_dashboard.html', {
        'total_users': total_users,
        'active_members': active_members,
        'inactive_members': inactive_members,
        'team_members': team_members,
        'announcements': announcements,
    })


def teammember_dashboard(request):
    # Get the logged-in team member
    team_member = User.objects.get(id=request.session['user_id'])
    team_name = team_member.team  

    # ✅ Show announcements from the team lead of this team, last 12 hrs only
    cutoff = timezone.now() - timedelta(hours=12)
    announcements = Announcement.objects.filter(
        created_by__team=team_name,   # announcements by team lead of this team
        created_at__gte=cutoff
    ).order_by('-created_at')

    return render(request, 'teammember_dashboard.html', {
        'announcements': announcements
    })
