import os
import uuid

# images upload path generator
def task_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    task_id = instance.task.id if instance.task.id else 'temp'
    folder = f'task_{task_id}'
    return os.path.join('task_images', folder, filename)

# avatar upload path generator
def avatar_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"avatar{ext}"
    return f'avatars/{instance.user.username}/{filename}'

# hello :D