from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# ------------------------------
# Contact / Feedback
# ------------------------------

class ContactMessage(models.Model):
    """
    Stores contact form submissions from users.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # auto-set when created

    def __str__(self):
        return f"{self.name} - {self.email}"


# ------------------------------
# Enrollment & Attendance
# ------------------------------

class Enrollment(models.Model):
    """
    Stores user enrollment details for membership and trainer selection.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=100)
    Email = models.EmailField()
    PhoneNumber = models.CharField(max_length=15)
    Gender = models.CharField(max_length=10)
    DOB = models.DateField(null=True, blank=True)
    Address = models.TextField(null=True, blank=True)
    SelectMembershipplan = models.CharField(max_length=50)
    SelectTrainer = models.CharField(max_length=50)
    paymentStatus = models.CharField(max_length=20, default="Pending")
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.FullName} ({self.user.username})"


class Attendance(models.Model):
    """
    Tracks daily attendance for gym members.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=now)  
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    workout_type = models.CharField(max_length=50)  # e.g., Biceps, Chest, etc.
    trainer = models.CharField(max_length=100, default='Unknown')

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Absent')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.workout_type}"


# ------------------------------
# Staff & Plans
# ------------------------------

class Trainer(models.Model):
    """
    Stores trainer information.
    """
    name = models.CharField(max_length=55)
    gender = models.CharField(max_length=25)
    phone = models.CharField(max_length=25)
    salary = models.IntegerField()
    specialization = models.CharField(max_length=100)
    image = models.ImageField(
        null=True,
        blank=True,
        default='assets/img/trainers/user_profile.jpg'
    )
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    """
    Stores different membership plans and their prices.
    """
    plan = models.CharField(max_length=185)
    price = models.IntegerField()

    def __int__(self):
        return self.id


# ------------------------------
# Testimonials
# ------------------------------

class Member(models.Model):
    """
    Stores testimonials/feedback from members.
    """
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default="Member")
    feedback = models.TextField()
    image = models.ImageField(
        upload_to='Uploads',
        blank=True,
        null=True,
        default='assets/img/trainers/user_profile.jpg'
    )

    def __str__(self):
        return self.name


# ------------------------------
# User Profile Extension
# ------------------------------

class Profile(models.Model):
    """
    Extends the default User model with extra details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
