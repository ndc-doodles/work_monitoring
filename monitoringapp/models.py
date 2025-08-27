from django.db import models
from datetime import timedelta
from django.utils import timezone



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return f"{self.name} ({self.department_name})"






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

    # Check if still valid (within 12 hours)
    def is_valid(self):
        return self.created_at >= timezone.now() - timedelta(hours=12)
