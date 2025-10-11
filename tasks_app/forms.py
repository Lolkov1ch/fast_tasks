from django import forms
from tasks_app.models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'creator']
