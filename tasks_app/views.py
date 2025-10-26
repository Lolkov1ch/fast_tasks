from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from tasks_app.mixins import UserIsOwnerMixin

from .forms import CommentForm, TaskFilterForm, TaskForm
from .models import Comment, CommentLike, Task, TaskImage

from django.views.generic import ListView
from django.db.models import Q
from .models import Task
from .forms import TaskFilterForm

class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all()
        
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            priority = form.cleaned_data.get("priority")
            due_date = form.cleaned_data.get("due_date")
            
            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if due_date:
                queryset = queryset.filter(due_date=due_date)
        
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        
        queryset = queryset.order_by('-id')
        return queryset
    
    def get(self, request, *args, **kwargs):
        if 'q' in request.GET and not request.GET.get('q'):
            return redirect('tasks_app:task_list')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        context["query"] = self.request.GET.get('q', '')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks_app:task_list")
    
    def post(self, request, *args, **kwargs):
        print("=" * 50)
        print("POST METHOD CALLED")
        print(f"POST data: {request.POST}")
        print(f"FILES: {request.FILES}")
        print(f"FILES.getlist('images'): {request.FILES.getlist('images')}")
        print("=" * 50)
        
        form = self.get_form()
       
        if form.is_valid():
            print("FORM IS VALID")
            task = form.save(commit=False)
            task.creator = request.user
            task.save()
            print(f"Task saved with ID: {task.id}")
            
            images = request.FILES.getlist('images')
            print(f"Files received: {len(images)}")
           
            for f in images:
                try:
                    print(f"Processing: {f.name}, size: {f.size} bytes")
                    TaskImage.objects.create(task=task, image=f)
                    print(f"Successfully saved: {f.name}")
                except Exception as e:
                    print(f"Error saving {f.name}: {e}")
                    import traceback
                    traceback.print_exc()
           
            return redirect(self.success_url)
        else:
            print(f"FORM IS INVALID")
            print(f"Form errors: {form.errors}")
            return self.render_to_response(self.get_context_data(form=form))

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks_app:task_list")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            task = form.save()

            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                TaskImage.objects.filter(id__in=delete_image_ids, task=task).delete()
                
            images = request.FILES.getlist('images')
            for f in images:
                TaskImage.objects.create(task=task, image=f)
            
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))
class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks_app:task_list")

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.object
            comment.save()
        return redirect("tasks_app:task_detail", pk=self.object.pk)
    
class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks_app:task_list")
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            task = form.save()

            delete_image_ids = request.POST.getlist('delete_images')
            if delete_image_ids:
                TaskImage.objects.filter(id__in=delete_image_ids, task=task).delete()
            
            images = request.FILES.getlist('images')
            for f in images:
                TaskImage.objects.create(task=task, image=f)
            
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class RegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks_app:task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "tasks/comment_form.html"

    def get_success_url(self):
        return reverse_lazy("tasks_app:task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "tasks/comment_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasks_app:task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            like.delete()
        return redirect("tasks_app:task_detail", pk=comment.task.pk)
        