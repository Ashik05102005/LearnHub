from django.db import models
from django.db.models import CASCADE
from django.conf import settings
from courses.models import Courses

# Create your models here.
class Enrollment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    student = models.ForeignKey(settings.AUTH_USER_MODEL ,
                                 on_delete=CASCADE ,
                                 related_name='enrollments')
    course = models.ForeignKey(Courses,on_delete=CASCADE ,
                               related_name='student_enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20 ,
        choices=Status.choices ,
        default=Status.PENDING
    )
    
