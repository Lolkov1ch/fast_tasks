from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Task, TaskImage
import os, shutil
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_delete, sender=Task)
def delete_task_images(sender, instance, **kwargs):
    for task_image in instance.images.all():
        if task_image.image and os.path.isfile(task_image.image.path):
            os.remove(task_image.image.path)

    folder_path = os.path.join(settings.MEDIA_ROOT, 'task_images', f'task_{instance.id}')
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)

@receiver(post_delete, sender=TaskImage)
def delete_taskimage_file(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(post_delete, sender=User)
def delete_user_avatar_folder(sender, instance, **kwargs):
    user_folder = os.path.join(settings.MEDIA_ROOT, f'avatars/{instance.username}')
    
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)