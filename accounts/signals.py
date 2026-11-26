from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.dispatch import receiver

User = get_user_model()

@receiver(post_save , sender=User)
def assign_student_group(sender,instance,created,**kwargs):
    if created :
        student_group , created_group = Group.objects.get_or_create(name='Student')
        instance.groups.add(student_group)
        print(f"Student group assigned to {instance.username}")
