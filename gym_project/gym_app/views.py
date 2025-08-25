# Django core imports
from django.shortcuts import render, redirect, get_list_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now

# Local models
from .models import ContactMessage, MembershipPlan, Trainer, Enrollment, Attendance, Member, Profile


# ------------------------------
# Public Pages
# ------------------------------

def home(request):
    """
    Display homepage with membership fees and testimonials.
    """
    fees = MembershipPlan.objects.all()
    testimonials = Member.objects.all()
    return render(request, 'index.html', {
        'fees': fees,
        'testimonials': testimonials,
    })


def about(request):
    """
    About us page.
    """
    return render(request, 'about.html')


def fees(request):
    """
    Membership fees page.
    """
    fees = MembershipPlan.objects.all()
    return render(request, 'fees.html', {'fees': fees})


def trainers(request):
    """
    Trainers page, ordered by latest added.
    """
    trainers = Trainer.objects.all().order_by("-timeStamp")
    return render(request, "trainers.html", {"trainers": trainers})


# ------------------------------
# Authentication
# ------------------------------

def signin(request):
    """
    User registration (sign up).
    """
    if request.method == 'POST':
        first_name = request.POST.get('name')
        username = request.POST.get('usernumber')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Password validation
        if pass1 != pass2:
            messages.error(request, 'Password must be same...')
            return redirect('signin')

        # Check for existing user
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already Used...')
            return redirect('signin')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Mobile Number already used...')
            return redirect('signin')

        # Create new user
        User.objects.create_user(
            first_name=first_name,
            username=username,
            email=email,
            password=pass1,
        )
        messages.success(request, 'Account successfully Created...')
        return redirect('login')

    return render(request, 'signin.html')


def login_user(request):
    """
    User login.
    """
    if request.method == 'POST':
        username = request.POST.get('usernumber')
        pass1 = request.POST.get('pass1')
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {request.user.username}! Time to push your limits and stay strong.")
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return redirect('login')

    return render(request, 'login.html')


def logout_user(request):
    """
    Logout the current user.
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please login first...')
        return redirect('home')

    logout(request)
    return redirect("home")


# ------------------------------
# Contact
# ------------------------------

def contact(request):
    """
    Contact form - stores message and optionally sends email.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if not message_text:
            messages.error(request, "Please enter a message!")
        else:
            # Save message to DB
            ContactMessage.objects.create(name=name, email=email, message=message_text)

            # Send email notification (optional)
            send_mail(
                subject=f"New message from {name}",
                message=f"Sender: {email}\n\nMessage:\n{message_text}",
                from_email='koni98882@gmail.com',
                recipient_list=['koni98882@gmail.com'],
            )

            messages.success(request, "Your message has been sent!")

    return render(request, "contact.html")


# ------------------------------
# Enrollment & Profile
# ------------------------------

def enroll(request):
    """
    Enroll a logged-in user into the gym.
    """
    if not request.user.is_authenticated:
        messages.error(request, "Please Login first...")
        return redirect('login')

    Membership = MembershipPlan.objects.all()
    SelectTrainer = Trainer.objects.all()
    context = {"Membership": Membership, "SelectTrainer": SelectTrainer}

    if request.method == "POST":
        FullName = request.POST.get('FullName')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        PhoneNumber = request.POST.get('PhoneNumber')
        DOB = request.POST.get('DOB')
        trainer = request.POST.get('trainer')
        address = request.POST.get('address')

        # Save enrollment
        Enrollment.objects.create(
            user=request.user,
            FullName=FullName,
            Email=email,
            Gender=gender,
            PhoneNumber=PhoneNumber,
            DOB=DOB,
            SelectTrainer=trainer,
            Address=address
        )

        messages.success(request, "Thanks For Enrollment")
        return redirect('profile')

    return render(request, "enroll.html", context)


def profile(request):
    """
    Display profile page with user's enrollment and attendance history.
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Please Login and Try Again")
        return redirect('/login')

    posts = Enrollment.objects.filter(user=request.user)
    attendance = Attendance.objects.filter(user=request.user)
    context = {"posts": posts, "attendance": attendance}
    return render(request, "profile.html", context)


# ------------------------------
# Attendance
# ------------------------------

def attendance(request):
    """
    Record daily attendance for the logged-in user.
    """
    if not request.user.is_authenticated:
        messages.warning(request, "Please login and try again.")
        return redirect('/login')

    SelectTrainer = Trainer.objects.all()
    context = {"SelectTrainer": SelectTrainer}

    if request.method == "POST":
        # Prevent duplicate attendance on the same day
        if Attendance.objects.filter(user=request.user, date=now().date()).exists():
            messages.warning(request, "You have already submitted attendance for today.")
            return redirect('/attendance')

        # Collect form data
        starting_time = request.POST.get('starting_time')
        ending_time = request.POST.get('ending_time')
        workout_type = request.POST.get('workout')
        trainer_name = request.POST.get('trainer')

        # Save attendance record
        Attendance.objects.create(
            user=request.user,
            starting_time=starting_time,
            ending_time=ending_time,
            workout_type=workout_type,
            trainer=trainer_name,
            status='Present'
        )

        messages.success(request, "Attendance recorded successfully.")
        return redirect('/attendance')

    return render(request, "attendance.html", context)
