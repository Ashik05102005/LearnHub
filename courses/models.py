from django.db import models
from django.conf import settings

# Create your models here.
class Courses(models.Model):
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL ,
        through='enrollments.Enrollment' , 
        related_name='enrollment_courses',
        blank=True
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL ,
        on_delete=models.CASCADE ,
        related_name='courses'
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title