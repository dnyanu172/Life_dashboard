from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import (
    Expense,
    Study,
    Habit,
    CalendarEvent,
    Goal
)
from .forms import (
    ExpenseForm,
    StudyForm,
    HabitForm,
    CalendarEventForm,
    GoalForm
)
# 🔹 REGISTER
def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')

    return render(request, 'accounts/register.html')


# 🔹 LOGIN
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

    return render(request, 'accounts/login.html')


#DASHBOARD

@login_required
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(
        user=user
    ).order_by('-date', '-created_at')

    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0


    today = timezone.localdate()

    today_expenses = expenses.filter(
        date=today
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0


    goals = Goal.objects.filter(
        user=user
    )

    total_goals = goals.count()

    completed_goals = goals.filter(
        status='Completed'
    ).count()


    habits = Habit.objects.filter(
        user=user
    )

    total_habits = habits.count()

    completed_habits = habits.filter(
        status='Completed'
    ).count()


    studies = Study.objects.filter(
        user=user
    )

    total_study_records = studies.count()

    recent_expenses = expenses[:5]


    context = {

        'name': user.username,

        'total_expenses': total_expenses,

        'today_expenses': today_expenses,

        'total_goals': total_goals,

        'completed_goals': completed_goals,

        'total_habits': total_habits,

        'completed_habits': completed_habits,

        'total_study_records': total_study_records,

        'recent_expenses': recent_expenses,

    }


    return render(
        request,
        'accounts/dashboard.html',
        context
    )

# LOGOUT
def logout(request):
    auth_logout(request)
    return redirect('login')

#Expense tracker
@login_required
def Expense_Tracker(request):

    user = request.user

    if request.method == "POST":

        form = ExpenseForm(request.POST)

        if form.is_valid():

            expense = form.save(commit=False)

            expense.user = user

            expense.save()

            return redirect('expenses')

    else:
        form = ExpenseForm()

    expenses = Expense.objects.filter(
        user=user
    ).order_by('-date', '-created_at')

    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    today = timezone.localdate()

    today_expenses = expenses.filter(
        date=today
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    start_of_week = today - timedelta(
        days=today.weekday()
    )

    week_expenses = expenses.filter(
        date__gte=start_of_week,
        date__lte=today
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    month_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'accounts/Expense Tracker.html',
        {
            'form': form,
            'expenses': expenses,
            'total_expenses': total_expenses,
            'month_expenses': month_expenses,
            'week_expenses': week_expenses,
            'today_expenses': today_expenses,
            'editing': False,
        }
    )


@login_required
def edit_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()
            return redirect('expenses')

    else:

        form = ExpenseForm(
            instance=expense
        )

    expenses = Expense.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')

    return render(
        request,
        'accounts/Expense Tracker.html',
        {
            'form': form,
            'expenses': expenses,
            'editing': True,
            'edit_expense': expense,
        }
    )


@login_required
def delete_expense(request, id):

    expense = get_object_or_404(
        Expense,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        expense.delete()

    return redirect('expenses')

#study tracker
@login_required
def Study_Tracker(request):

    user = request.user

    # ADD STUDY
    if request.method == "POST":

        form = StudyForm(request.POST)

        if form.is_valid():

            study = form.save(commit=False)

            study.user = user

            study.save()

            return redirect('study')

    else:

        form = StudyForm()


    # USER'S STUDY DATA ONLY
    studies = Study.objects.filter(
        user=user
    ).order_by('-date', '-created_at')


    # TOTAL STUDY HOURS
    total_hours = studies.aggregate(
        total=Sum('hours')
    )['total'] or 0


    today = timezone.localdate()


    # TODAY'S HOURS
    today_hours = studies.filter(
        date=today
    ).aggregate(
        total=Sum('hours')
    )['total'] or 0


    # THIS WEEK
    start_of_week = today - timedelta(
        days=today.weekday()
    )

    week_hours = studies.filter(
        date__gte=start_of_week,
        date__lte=today
    ).aggregate(
        total=Sum('hours')
    )['total'] or 0


    # THIS MONTH
    month_hours = studies.filter(
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum('hours')
    )['total'] or 0


    context = {

        'form': form,

        'studies': studies,

        'total_hours': total_hours,

        'today_hours': today_hours,

        'week_hours': week_hours,

        'month_hours': month_hours,

        'editing': False,
    }


    return render(
        request,
        'accounts/Study Tracker.html',
        context
    )
@login_required
def edit_study(request, id):

    study = get_object_or_404(
        Study,
        id=id,
        user=request.user
    )


    if request.method == "POST":

        form = StudyForm(
            request.POST,
            instance=study
        )

        if form.is_valid():

            form.save()

            return redirect('study')

    else:

        form = StudyForm(
            instance=study
        )


    studies = Study.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')


    return render(
        request,
        'accounts/Study Tracker.html',
        {
            'form': form,
            'studies': studies,
            'editing': True,
            'edit_study': study,
        }
    )
@login_required
def delete_study(request, id):

    study = get_object_or_404(
        Study,
        id=id,
        user=request.user
    )

    if request.method == "POST":
        study.delete()

    return redirect('study')

#habit tracker
@login_required
def Habit_Tracker(request):

    user = request.user

    # ADD HABIT
    if request.method == "POST":

        form = HabitForm(request.POST)

        if form.is_valid():

            habit = form.save(commit=False)

            habit.user = user

            habit.save()

            return redirect('habit')

    else:

        form = HabitForm()


    # USER'S HABITS ONLY
    habits = Habit.objects.filter(
        user=user
    ).order_by('-date', '-created_at')


    # TOTAL HABITS
    total_habits = habits.count()


    # COMPLETED HABITS
    completed_habits = habits.filter(
        status='Completed'
    ).count()


    # PENDING HABITS
    pending_habits = habits.filter(
        status='Pending'
    ).count()


    # IN PROGRESS
    progress_habits = habits.filter(
        status='In Progress'
    ).count()


    context = {

        'form': form,

        'habits': habits,

        'total_habits': total_habits,

        'completed_habits': completed_habits,

        'pending_habits': pending_habits,

        'progress_habits': progress_habits,

        'editing': False,

    }


    return render(
        request,
        'accounts/Habit Tracker.html',
        context
    )
@login_required
def edit_habit(request, id):

    habit = get_object_or_404(
        Habit,
        id=id,
        user=request.user
    )


    if request.method == "POST":

        form = HabitForm(
            request.POST,
            instance=habit
        )

        if form.is_valid():

            form.save()

            return redirect('habit')

    else:

        form = HabitForm(
            instance=habit
        )


    habits = Habit.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')


    return render(
        request,
        'accounts/Habit Tracker.html',
        {
            'form': form,
            'habits': habits,
            'editing': True,
            'edit_habit': habit,
        }
    )

@login_required
def delete_habit(request, id):

    habit = get_object_or_404(
        Habit,
        id=id,
        user=request.user
    )


    if request.method == "POST":
        habit.delete()

    return redirect('habit')

#calendar
@login_required
def Calendar(request):

    user = request.user

    # ADD EVENT
    if request.method == "POST":

        form = CalendarEventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)

            event.user = user

            event.save()

            return redirect('calendar')

    else:

        form = CalendarEventForm()


    # USER'S EVENTS ONLY
    events = CalendarEvent.objects.filter(
        user=user
    ).order_by('date', 'time')


    context = {

        'form': form,

        'events': events,

        'editing': False,

    }


    return render(
        request,
        'accounts/Calendar.html',
        context
    )

@login_required
def edit_calendar_event(request, id):

    event = get_object_or_404(
        CalendarEvent,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = CalendarEventForm(
            request.POST,
            instance=event
        )

        if form.is_valid():

            form.save()

            return redirect('calendar')

    else:

        form = CalendarEventForm(
            instance=event
        )


    events = CalendarEvent.objects.filter(
        user=request.user
    ).order_by('date', 'time')


    return render(
        request,
        'accounts/Calendar.html',
        {
            'form': form,
            'events': events,
            'editing': True,
            'edit_event': event,
        }
    )

@login_required
def delete_calendar_event(request, id):

    event = get_object_or_404(
        CalendarEvent,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        event.delete()

    return redirect('calendar')

#goals
@login_required
def Goals(request):

    user = request.user

    # ADD GOAL
    if request.method == "POST":

        form = GoalForm(request.POST)

        if form.is_valid():

            goal = form.save(commit=False)

            goal.user = user

            goal.save()

            return redirect('goals')

    else:

        form = GoalForm()


    # USER'S GOALS ONLY
    goals = Goal.objects.filter(
        user=user
    ).order_by('target_date', '-created_at')


    # TOTAL
    total_goals = goals.count()


    # COMPLETED
    completed_goals = goals.filter(
        status='Completed'
    ).count()


    # IN PROGRESS
    progress_goals = goals.filter(
        status='In Progress'
    ).count()


    # NOT STARTED
    pending_goals = goals.filter(
        status='Not Started'
    ).count()


    context = {

        'form': form,

        'goals': goals,

        'total_goals': total_goals,

        'completed_goals': completed_goals,

        'progress_goals': progress_goals,

        'pending_goals': pending_goals,

        'editing': False,

    }


    return render(
        request,
        'accounts/Goals.html',
        context
    )
@login_required
def edit_goal(request, id):

    goal = get_object_or_404(
        Goal,
        id=id,
        user=request.user
    )


    if request.method == "POST":

        form = GoalForm(
            request.POST,
            instance=goal
        )

        if form.is_valid():

            form.save()

            return redirect('goals')

    else:

        form = GoalForm(
            instance=goal
        )


    goals = Goal.objects.filter(
        user=request.user
    ).order_by('target_date', '-created_at')


    return render(
        request,
        'accounts/Goals.html',
        {
            'form': form,
            'goals': goals,
            'editing': True,
            'edit_goal': goal,
        }
    )

@login_required
def delete_goal(request, id):

    goal = get_object_or_404(
        Goal,
        id=id,
        user=request.user
    )


    if request.method == "POST":
        goal.delete()

    return redirect('goals')

#reports

@login_required
def Reports(request):

    user = request.user


    expenses = Expense.objects.filter(
        user=user
    ).order_by('-date', '-created_at')


    total_expenses = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0


    total_expense_records = expenses.count()


    studies = Study.objects.filter(
        user=user
    )


    total_study_records = studies.count()


    try:

        total_study_hours = studies.aggregate(
            total=Sum('hours')
        )['total'] or 0

    except Exception:

        total_study_hours = 0

    habits = Habit.objects.filter(
        user=user
    )


    total_habits = habits.count()


    completed_habits = habits.filter(
        status='Completed'
    ).count()


    pending_habits = habits.filter(
        status='Pending'
    ).count()


    progress_habits = habits.filter(
        status='In Progress'
    ).count()

    goals = Goal.objects.filter(
        user=user
    )


    total_goals = goals.count()


    completed_goals = goals.filter(
        status='Completed'
    ).count()


    progress_goals = goals.filter(
        status='In Progress'
    ).count()


    pending_goals = goals.filter(
        status='Not Started'
    ).count()


    context = {

        'expenses': expenses[:10],

        'total_expenses': total_expenses,

        'total_expense_records': total_expense_records,

        'total_study_records': total_study_records,

        'total_study_hours': total_study_hours,

        'total_habits': total_habits,

        'completed_habits': completed_habits,

        'pending_habits': pending_habits,

        'progress_habits': progress_habits,

        'total_goals': total_goals,

        'completed_goals': completed_goals,

        'progress_goals': progress_goals,

        'pending_goals': pending_goals,

    }


    return render(
        request,
        'accounts/Reports.html',
        context
    )

try:
    total_study_hours = studies.aggregate(
        total=Sum('hours')
    )['total'] or 0
except Exception:
    total_study_hours = 0

#setting
@login_required
def Settings(request):

    user = request.user

    message = None
    error = None

    if request.method == "POST":

        action = request.POST.get('action')

        if action == "profile":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            message = "Profile updated successfully."

        elif action == "password":
            current_password = request.POST.get(
                'current_password'
            )

            new_password = request.POST.get(
                'new_password'
            )

            confirm_password = request.POST.get(
                'confirm_password'
            )


            if not user.check_password(
                current_password
            ):

                error = "Current password is incorrect."


            elif new_password != confirm_password:

                error = "New passwords do not match."


            elif len(new_password) < 6:

                error = "Password must be at least 6 characters."


            else:

                user.set_password(new_password)

                user.save()

                auth_login(
                    request,
                    user
                )

                message = "Password changed successfully."

    context = {
        'user': user,
        'message': message,
        'error': error,
    }

    return render(
        request,
        'accounts/Settings.html',
        context
    )
