from .models import Comment
from django import forms

from .models import Task, TaskImage


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All')] + Task.STATUS_CHOICES,
        required=False,
        label='Status'
    )

    priority = forms.ChoiceField(
        choices=[('', 'All')] + Task.PRIORITY_CHOICES,
        required=False,
        label='Priority'
    )

    due_date = forms.DateField(
        required=False,
        label='Due Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class TaskImageForm(forms.ModelForm):
    class Meta:
        model = TaskImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}),
        }

