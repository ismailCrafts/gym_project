"""
URL configuration for the Gym Management app.
Each path maps a URL route to its corresponding view function.
"""

from django.urls import path
from . import views


urlpatterns = [
    # ------------------------------
    # Public Pages
    # ------------------------------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('fees/', views.fees, name='fees'),
    path('trainers/', views.trainers, name='trainers'),
    path('contact/', views.contact, name='contact'),

    # ------------------------------
    # Authentication
    # ------------------------------
    path('signin/', views.signin, name='signin'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout_user'),

    # ------------------------------
    # User Features
    # ------------------------------
    path('enroll/', views.enroll, name='enroll'),
    path('profile/', views.profile, name='profile'),
    path('attendance/', views.attendance, name='attendance'),
]
