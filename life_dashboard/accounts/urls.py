"""
URL configuration for life_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('expenses/', views.Expense_Tracker, name='expenses'),
    path('expenses/edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('expenses/delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('study/', views.Study_Tracker, name='study'),
    path('study/edit/<int:id>/', views.edit_study, name='edit_study'),
    path('study/delete/<int:id>/', views.delete_study, name='delete_study'),
    path('habit/', views.Habit_Tracker, name='habit'),
    path('habit/edit/<int:id>/', views.edit_habit, name='edit_habit'),
    path('habit/delete/<int:id>/', views.delete_habit, name='delete_habit'),
    path('calendar/', views.Calendar, name='calendar'),
    path('calendar/edit/<int:id>/', views.edit_calendar_event, name='edit_calendar_event'),
    path('calendar/delete/<int:id>/', views.delete_calendar_event, name='delete_calendar_event'),
    path('goals/', views.Goals, name='goals'),
    path('goals/edit/<int:id>/', views.edit_goal, name='edit_goal'),
    path('goals/delete/<int:id>/', views.delete_goal, name='delete_goal'),
    path('reports/', views.Reports, name='reports'),
    path('settings/', views.Settings, name='settings'),
    path('logout/', views.logout, name='logout'),
]