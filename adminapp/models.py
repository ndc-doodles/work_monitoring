from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

class User(models.Model):
    ROLE_CHOICES = [('Team Lead', 'Team Lead'), ('Team Member', 'Team Member')]
    STATUS_CHOICES = [('Online', 'Online'), ('Idle', 'Idle'), ('Offline', 'Offline')]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Offline')
    current_project = models.CharField(max_length=200, blank=True)  


class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('morning', 'Morning'),
        ('evening', 'Evening'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)  # <-- New field
    type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    content = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - {self.type} - {self.submitted_at.date()}"
    


class AssignedProject(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_projects')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    project_name = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100)  # Client, Company, Template, etc.
    category = models.CharField(max_length=100, blank=True, null=True)  # Optional (e.g. Static, Poster)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    date_assigned = models.DateField(default=timezone.now)
    
    additional_notes = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return f"{self.project_name} → {self.assigned_to}"