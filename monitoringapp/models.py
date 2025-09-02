from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
       return self.name







class User(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=150)
    employee_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
  

    job_Position = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    work_location = models.CharField(max_length=150, blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.designation})"
    

class Announcement(models.Model):
    title = models.CharField(max_length=200)  
    message = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  
    is_active = models.BooleanField(default=True)  

    class Meta:
        ordering = ['-created_at']  

    def __str__(self):
        return self.title

    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(hours=12)



class MorningReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=150)
    team = models.CharField(max_length=150)
    report_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Morning Report - {self.user.username} ({self.created_at.date()})"


class EveningReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=150)
    team = models.CharField(max_length=150)
    report_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Evening Report - {self.user.username} ({self.created_at.date()})"
    


class ProjectAssign(models.Model):
    WORK_TYPE_CHOICES = (
        ("Client", "Client"),
        ("Company", "Company"),
        ("Other", "Other"),
    )
    PRIORITY_CHOICES = (
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Urgent", "Urgent"),
    )

    team = models.ForeignKey("Team", on_delete=models.CASCADE)  # auto-filled
    department = models.ForeignKey("Department", on_delete=models.CASCADE)  # dropdown
    assign_to = models.ForeignKey(
        "User", related_name="assigned_works", on_delete=models.CASCADE
    )  # only same team members
    assigned_by = models.ForeignKey(
        "User", related_name="given_works", on_delete=models.CASCADE
    )  # the logged-in team lead
    
    work_name = models.CharField(max_length=255)
    work_type = models.CharField(max_length=50, choices=WORK_TYPE_CHOICES)
    category = models.CharField(max_length=255, blank=True, null=True)  # optional
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    additional_notes = models.TextField(blank=True, null=True)

    upload_file = models.FileField(upload_to="uploads/files/", blank=True, null=True)
    upload_image = models.ImageField(upload_to="uploads/images/", blank=True, null=True)

    color_preference = models.CharField(max_length=100, blank=True, null=True)
    content_example = models.TextField(blank=True, null=True)

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="Medium")
    assigned_date = models.DateField(default=now)

    def __str__(self):
        return f"{self.work_name} → {self.assign_to.name}"