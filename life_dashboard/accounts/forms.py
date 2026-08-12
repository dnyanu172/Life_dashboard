from django import forms
from .models import (
    Expense,
    Study,
    Habit,
    CalendarEvent,
    Goal
)

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense

        fields = [
            'title',
            'amount',
            'category',
            'date'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'step': '0.01'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }

class StudyForm(forms.ModelForm):

    class Meta:
        model = Study

        fields = [
            'subject',
            'topic',
            'hours',
            'date',
            'status'
        ]

        widgets = {

            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),

            'topic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter topic'
            }),

            'hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter study hours',
                'step': '0.5'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
class HabitForm(forms.ModelForm):

    class Meta:
        model = Habit

        fields = [
            'name',
            'description',
            'date',
            'status'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter habit name'
            }),

            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class CalendarEventForm(forms.ModelForm):

    class Meta:
        model = CalendarEvent

        fields = [
            'title',
            'description',
            'date',
            'time'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),

            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description'
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
        }

class GoalForm(forms.ModelForm):

    class Meta:
        model = Goal

        fields = [
            'title',
            'description',
            'target_date',
            'status'
        ]

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter goal title'
            }),

            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter goal description'
            }),

            'target_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }