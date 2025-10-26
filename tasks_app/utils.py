import os
import uuid

# images upload path generator
def task_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    task_id = instance.task.id if instance.task.id else 'temp'
    folder = f'task_{task_id}'
    return os.path.join('task_images', folder, filename)

# hello :D