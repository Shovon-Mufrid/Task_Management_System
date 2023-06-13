from django.db.models.signals import pre_save
from django.dispatch import receiver
from App_Project.models import Task

@receiver(pre_save, sender=Task)
def update_task_status(sender, instance, **kwargs):
    if instance.pk:  # Check if the task is being updated
        old_task = Task.objects.get(pk=instance.pk)
        if old_task.status != instance.status:
            # Task status has changed
            # Perform any necessary actions or updates here
            pass