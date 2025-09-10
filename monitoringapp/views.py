from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  
from .models import *
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import openpyxl
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password, make_password
import random
from django.core.mail import send_mail
from datetime import time, timedelta











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


@csrf_exempt

def admin_usermanagement(request):
    users = User.objects.all()
    departments = Department.objects.all()
    teams = Team.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("id")  # for edit, will be None for new users
        name = request.POST.get("name")
        employee_id = request.POST.get("employee_id")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        department_name = request.POST.get("department")
        team_name = request.POST.get("team")
        job_Position = request.POST.get("job_Position")
        designation = request.POST.get("designation")
        work_location = request.POST.get("work_location")
        username = request.POST.get("username")
        password = request.POST.get("password")
        status = request.POST.get("status")
        image = request.FILES.get("profile_image")

        department = get_object_or_404(Department, name=department_name) if department_name else None
        team = get_object_or_404(Team, name=team_name) if team_name else None

        if user_id:  # Edit existing user
            user = get_object_or_404(User, id=user_id)

            # Check uniqueness for employee_id and username, excluding current user
            if User.objects.filter(employee_id=employee_id).exclude(id=user.id).exists():
                messages.error(request, "⚠️ Employee ID already exists for another user.")
                return redirect("admin_usermanagement")

            if User.objects.filter(username=username).exclude(id=user.id).exists():
                messages.error(request, "⚠️ Username already exists for another user.")
                return redirect("admin_usermanagement")

            # Update user
            user.name = name
            user.employee_id = employee_id
            user.email = email
            user.phone = phone
            user.department = department
            user.team = team
            user.job_Position = job_Position
            user.designation = designation
            user.work_location = work_location
            user.username = username
            user.password = password
            user.status = status
            if image:
                user.profile_image = image
            user.save()
            messages.success(request, "✅ User updated successfully!")
        
        else:  # Create new user
            if User.objects.filter(employee_id=employee_id).exists():
                messages.error(request, "⚠️ Employee ID already exists. Please choose another one.")
                return redirect("admin_usermanagement")

            if User.objects.filter(username=username).exists():
                messages.error(request, "⚠️ Username already exists. Please choose another one.")
                return redirect("admin_usermanagement")

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
                username=username,
                password=password,
                status=status,
                profile_image=image
            )
            messages.success(request, "✅ User created successfully!")

        return redirect("admin_usermanagement")

    context = {
        "users": users,
        "departments": departments,
        "teams": teams,
    }
    return render(request, "admin_usermanagement.html", context)

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

        # Department + Team (FKs)
        department_name = request.POST.get("edit_department")
        team_name = request.POST.get("edit_team")

        if department_name:
            try:
                user.department = Department.objects.get(name=department_name)
            except Department.DoesNotExist:
                user.department = None

        if team_name:
            try:
                user.team = Team.objects.get(name=team_name)
            except Team.DoesNotExist:
                user.team = None

        user.job_Position = request.POST.get("edit_job_position")
        user.designation = request.POST.get("edit_designation")
        user.work_location = request.POST.get("edit_work_location")
        user.username = request.POST.get("edit_username")
        user.status = request.POST.get("edit_status")

        # 🔐 Handle password (hash it!)
        password = request.POST.get("edit_password")
        if password:
            user.password = make_password(password)

        # Joining Date
        joining_date = request.POST.get("edit_joining_date")
        if joining_date:
            try:
                user.joining_date = datetime.strptime(joining_date, "%Y-%m-%d").date()
            except ValueError:
                messages.error(request, "Invalid date format! Use YYYY-MM-DD.")
                return redirect("admin_usermanagement")
        else:
            user.joining_date = None

        # Profile Image
        if request.FILES.get("edit_profile_upload"):
            user.profile_image = request.FILES["edit_profile_upload"]

        user.save()
        messages.success(request, "User updated successfully!")
        return redirect("admin_usermanagement")

    return redirect("admin_usermanagement")


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




def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_otp'] = str(otp)

            # Send OTP via email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is {otp}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, "OTP sent to your email")
            return redirect("verify_otp")

        except User.DoesNotExist:
            messages.error(request, "Email not registered")
    
    return render(request, "forgot_password.html")


# Step 2: Verify OTP
def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get("otp")
        if otp == request.session.get("reset_otp"):
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")

    return render(request, "verify_otp.html")


# Step 3: Reset Password
def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            email = request.session.get("reset_email")
            user = User.objects.get(email=email)
            user.password = password   # ⚠️ Better: use user.set_password(password) if using Django's auth User
            user.save()

            # Clear session values
            request.session.pop("reset_email", None)
            request.session.pop("reset_otp", None)

            messages.success(request, "Password reset successful. Please login.")
            return redirect("login")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "reset_password.html")








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

    team_members = User.objects.filter(team=team_lead.team)


    total_users = team_members.count()
    active_members = team_members.filter(status="active").count()
    inactive_members = team_members.filter(status="inactive").count()

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

def is_within_time_range(start_time, end_time, now=None):
    now = now or timezone.localtime().time()
    return start_time <= now <= end_time

def teammember_dashboard(request):
    team_member = User.objects.get(id=request.session['user_id'])
    team_name = team_member.team  

    cutoff = timezone.now() - timedelta(hours=12)
    announcements = Announcement.objects.filter(
        created_by__team=team_name,   
        created_at__gte=cutoff
    ).order_by('-created_at')

    morning_start, morning_end = time(9, 30), time(10, 30)
    evening_start, evening_end = time(17, 0), time(18, 15)

    if request.method == "POST":
        now_time = timezone.localtime().time()

        if 'morning_submit' in request.POST:
            if is_within_time_range(morning_start, morning_end, now_time):
                report_text = request.POST.get("morning_report")
                status = request.POST.get("morning_status")
                if report_text and status:
                    MorningReport.objects.create(
                        user=team_member,
                        department=team_member.department.name if team_member.department else None,
                        team=team_member.team.name if team_member.team else None,
                        report_text=report_text,
                        status=status
                    )
                    messages.success(request, "Morning report submitted successfully.")
                    return redirect('teammember_dashboard')
            else:
                messages.error(request, "You can only submit morning reports between 9:30 and 10:30 AM.")

        elif 'evening_submit' in request.POST:
            if is_within_time_range(evening_start, evening_end, now_time):
                report_text = request.POST.get("evening_report")
                status = request.POST.get("evening_status")
                if report_text and status:
                    EveningReport.objects.create(
                        user=team_member,
                        department=team_member.department.name if team_member.department else None,
                        team=team_member.team.name if team_member.team else None,
                        report_text=report_text,
                        status=status
                    )
                    messages.success(request, "Evening report submitted successfully.")
                    return redirect('teammember_dashboard')
            else:
                messages.error(request, "You can only submit evening reports between 5:00 and 6:15 PM.")

    return render(request, 'teammember_dashboard.html', {
        'announcements': announcements,
        'morning_allowed': is_within_time_range(morning_start, morning_end),
        'evening_allowed': is_within_time_range(evening_start, evening_end),
    })
def teamlead_reports(request):
    team_lead = get_object_or_404(User, id=request.session['user_id'])
    team_name = team_lead.team
    show_all = request.GET.get('all') == '1'

    # Filter reports (today or all)
    if show_all:
        morning_reports = MorningReport.objects.filter(team=team_name).order_by('-created_at')
        evening_reports = EveningReport.objects.filter(team=team_name).order_by('-created_at')
    else:
        today = date.today()
        morning_reports = MorningReport.objects.filter(team=team_name, created_at__date=today)
        evening_reports = EveningReport.objects.filter(team=team_name, created_at__date=today)

    # Handle Excel export
    if 'export' in request.GET:
        wb = Workbook()
        ws = wb.active
        ws.title = "Team Reports"

        # Set headers (added Status column)
        headers = ["Date", "Time", "Report Type", "Name", "Team", "Department", "Report", "Status"]
        ws.append(headers)

        # Function to add reports to Excel
        def add_reports(report_list, report_type):
            for report in report_list:
                local_time = timezone.localtime(report.created_at)  # Convert UTC → Local
                ws.append([
                    local_time.strftime("%Y-%m-%d"),
                    local_time.strftime("%I:%M %p"),
                    report_type,
                    getattr(report.user, "name", report.user.username),  # Safe fallback
                    report.team,
                    report.department,
                    report.report_text,
                    report.status
                ])

        # Add both Morning & Evening Reports
        add_reports(morning_reports, "Morning")
        add_reports(evening_reports, "Evening")

        # Apply text wrap to 'Report' column
        for row in ws.iter_rows(min_row=2, min_col=7, max_col=7):
            for cell in row:
                cell.alignment = Alignment(wrap_text=True, vertical='top')

        # Adjust column widths for readability
        column_widths = [15, 12, 12, 20, 15, 20, 50, 15]
        for i, width in enumerate(column_widths, start=1):
            ws.column_dimensions[ws.cell(row=1, column=i).column_letter].width = width

        # Return Excel file as response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename="team_reports.xlsx"'
        wb.save(response)
        return response

    return render(request, 'teamlead_reports.html', {
        'morning_reports': morning_reports,
        'evening_reports': evening_reports,
        'show_all': show_all
    })
def teamlead_project_assigning(request):
    team_lead = get_object_or_404(User, id=request.session["user_id"])
    departments = Department.objects.all()

    # Fetch all users in same team, who are team members
    # Use __icontains instead of __iexact to avoid case mismatch
    team_members = User.objects.filter(
        team=team_lead.team,
        job_Position__icontains='team member'
    ).exclude(id=team_lead.id)

    if request.method == "POST":
        ProjectAssign.objects.create(
            team=team_lead.team,
            department_id=request.POST.get("department"),
            assign_to_id=request.POST.get("assign_to"),
            assigned_by=team_lead,
            work_name=request.POST.get("work_name"),
            work_type=request.POST.get("work_type"),
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            deadline=request.POST.get("deadline"),
            additional_notes=request.POST.get("additional_notes"),
            upload_file=request.FILES.get("upload_file"),
            upload_image=request.FILES.get("upload_image"),
            color_preference=request.POST.get("color_preference"),
            content_example=request.POST.get("content_example"),
            priority=request.POST.get("priority"),
        )
        return redirect("teamlead_project_assigning")

    projects = ProjectAssign.objects.filter(team=team_lead.team)

    return render(request, "teamlead_project_assigning.html", {
        "departments": departments,
        "team_lead": team_lead,
        "team_members": team_members,
        "projects": projects,
    })


def project_assign_edit(request, pk):
    project = get_object_or_404(ProjectAssign, id=pk)
    departments = Department.objects.all()
    team_members = User.objects.filter(
        team=project.team, job_Position__iexact='Team Member'
    ).exclude(id=project.assigned_by.id)

    if request.method == "POST":
        project.department_id = request.POST.get("department")
        project.assign_to_id = request.POST.get("assign_to")
        project.work_name = request.POST.get("work_name")
        project.work_type = request.POST.get("work_type")
        project.category = request.POST.get("category")
        project.description = request.POST.get("description")

        # ✅ Handle deadline properly
        deadline = request.POST.get("deadline")
        project.deadline = deadline if deadline else None

        project.additional_notes = request.POST.get("additional_notes")

        if request.FILES.get("upload_file"):
            project.upload_file = request.FILES.get("upload_file")
        if request.FILES.get("upload_image"):
            project.upload_image = request.FILES.get("upload_image")

        project.color_preference = request.POST.get("color_preference")
        project.content_example = request.POST.get("content_example")
        project.priority = request.POST.get("priority")

        project.save()
        return redirect("teamlead_project_assigning")

    return render(request, "teamlead_project_assigning.html", {
        "project": project,
        "departments": departments,
        "team_members": team_members,
    })


def project_assign_delete(request, pk):
    project = get_object_or_404(ProjectAssign, id=pk)
    project.delete()
    return redirect("teamlead_project_assigning")


def teammember_project(request):
    user = get_object_or_404(User, id=request.session["user_id"])
    projects = ProjectAssign.objects.filter(assign_to=user).order_by("-assigned_date")
    return render(request, "teammember_project.html", {"projects": projects})

def teamlead_notepad(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    # All notes for this user
    all_notes = Notepad.objects.filter(user=user).order_by("-updated_at")

    # Pagination (4 notes per page)
    paginator = Paginator(all_notes, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Note to edit/view
    note_id = request.GET.get("note_id")
    note = None
    if note_id:
        try:
            note = Notepad.objects.get(id=note_id, user=user)
        except Notepad.DoesNotExist:
            note = None  # If invalid ID, open new note

    if request.method == "POST":
        note_id_post = request.POST.get("note_id")
        title = request.POST.get("title") or "Untitled"
        content = request.POST.get("content")

        if note_id_post:
            # Update existing note
            note = get_object_or_404(Notepad, id=note_id_post, user=user)
            note.title = title
            note.content = content
            note.save()
        else:
            # Create new note
            note = Notepad.objects.create(user=user, title=title, content=content)

        return redirect(f"{request.path}?note_id={note.id}")

    return render(request, "teamlead_notepad.html", {"note": note, "page_obj": page_obj})

def teammember_notepad(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    # All notes for this user
    all_notes = Notepad.objects.filter(user=user).order_by("-updated_at")

    # Pagination (4 notes per page)
    paginator = Paginator(all_notes, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Note to edit/view
    note_id = request.GET.get("note_id")
    note = None
    if note_id:
        try:
            note = Notepad.objects.get(id=note_id, user=user)
        except Notepad.DoesNotExist:
            note = None  # If invalid ID, open new note

    if request.method == "POST":
        note_id_post = request.POST.get("note_id")
        title = request.POST.get("title") or "Untitled"
        content = request.POST.get("content")

        if note_id_post:
            # Update existing note
            note = get_object_or_404(Notepad, id=note_id_post, user=user)
            note.title = title
            note.content = content
            note.save()
        else:
            # Create new note
            note = Notepad.objects.create(user=user, title=title, content=content)

        return redirect(f"{request.path}?note_id={note.id}")

    return render(request, "teammember_notepad.html", {"note": note, "page_obj": page_obj})




def teamlead_repository(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        file = request.FILES.get("file")

        Knowledge.objects.create(
            department=user.department,
            user=user,
            title=title,
            description=description,
            link=link,
            file=file
        )
        return redirect("teamlead_repository")

    knowledge_items = Knowledge.objects.filter(department=user.department).order_by("-created_at")

    return render(request, "teamlead_repository.html", {"knowledge_items": knowledge_items})


def teamlead_repository_delete(request, pk):
    user = get_object_or_404(User, id=request.session.get("user_id"))
    resource = get_object_or_404(Knowledge, id=pk, department=user.department)

    if request.method == "POST":
        resource.delete()
        return redirect("teamlead_repository")



def teammember_repository(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        file = request.FILES.get("file")

        Knowledge.objects.create(
            department=user.department,
            user=user,
            title=title,
            description=description,
            link=link,
            file=file
        )
        return redirect("teammember_repository")

    knowledge_items = Knowledge.objects.filter(department=user.department).order_by("-created_at")

    return render(request, "teammember_repository.html", {"knowledge_items": knowledge_items})



@login_required
def teammember_repository_delete(request, pk):
    user = get_object_or_404(User, id=request.session.get("user_id"))
    resource = get_object_or_404(Knowledge, id=pk, department=user.department)

    if request.method == "POST":
        resource.delete()
        return redirect("teammember_repository")



def teamlead_profile(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    if request.method == "POST":
        action = request.POST.get("action")

        # ✅ Change Password
        if action == "change_password":
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not check_password(current_password, user.password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New password and confirmation do not match.")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully!")

        # ✅ Edit Profile
        elif action == "edit_profile":
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.phone = request.POST.get("phone")
            user.work_location = request.POST.get("work_location")

            if "profile_image" in request.FILES:
                user.profile_image = request.FILES["profile_image"]

            user.save()
            messages.success(request, "Profile updated successfully!")

        return redirect("teamlead_profile")

    return render(request, "teamlead_profile.html", {"user": user})

def teammember_profile(request):
    user = get_object_or_404(User, id=request.session.get("user_id"))

    if request.method == "POST":
        action = request.POST.get("action")

        # ✅ Change Password
        if action == "change_password":
            current_password = request.POST.get("current_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not check_password(current_password, user.password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New password and confirmation do not match.")
            else:
                user.password = make_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully!")

        # ✅ Edit Profile
        elif action == "edit_profile":
            user.name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.phone = request.POST.get("phone")
            user.work_location = request.POST.get("work_location")

            if "profile_image" in request.FILES:
                user.profile_image = request.FILES["profile_image"]

            user.save()
            messages.success(request, "Profile updated successfully!")

        return redirect("teammember_profile")

    return render(request, "teammember_profile.html", {"user": user})

def teammember_task(request):
    return render(request,'teammember_task.html')