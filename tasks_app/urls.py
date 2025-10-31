from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tasks_app import views
from .views import (
                    TaskListView, 
                    TaskDetailView, 
                    TaskCreateView, 
                    TaskUpdateView, 
                    RegisterView, 
                    TaskDeleteView, 
                    CommentEditView, 
                    CommentDeleteView, 
                    ToggleLikeView, 
                    UserSettingsView, 
                    UserProfileView, 
                    DeleteAccountConfirmView
                    )

app_name = "tasks_app"

urlpatterns = [
    path("", TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("add/", TaskCreateView.as_view(), name="task_create"),


    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    
    path('settings/', UserSettingsView.as_view(), name='settings'),
    
    path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),

    path('register/', RegisterView.as_view(), name='register'),
    
    path('delete_account/', DeleteAccountConfirmView.as_view(), name='delete_account'),

    path("comment/<int:pk>/edit/", CommentEditView.as_view(), name="comment_edit"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path("comment/<int:pk>/like/", ToggleLikeView.as_view(), name="comment_like"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)