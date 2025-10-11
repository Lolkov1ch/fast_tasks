from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from tasks_app import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView   
from tasks_app.forms import TaskForm

class TaskListView(ListView):
    model = models.Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10    

class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(CreateView):
    model = models.Task
    template_name = 'tasks/task_form.html'
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task_list")
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)




