from django.urls import path
from tasks_app import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("create/", views.TaskCreateView.as_view(), name="task_create"),
]
