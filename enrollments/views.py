from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from courses.models import Courses
from .models import Enrollment
from django.contrib import messages

# Create your views here.
@login_required
def enroll_course(request,course_id):
    course = get_object_or_404(Courses,id = course_id)

    existing_enrollments = Enrollment.objects.filter(
        student = request.user,
        course = course
    ).exists()

    if existing_enrollments :
        messages.warning(request,"Already enrolled in this course")
        return redirect('course_list')

    Enrollment.objects.create(
        student = request.user , 
        course = course
    )

    messages.success(request,"Enrollment request sent successfully")

    return redirect('course_list')

@login_required
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(student = request.user).select_related('course','course__instructor')
    return render(request , 'my_enrollment.html',{'enrollments':enrollments})

def cancel_enrollment(request , enrollment_id):
    enrollment = get_object_or_404(Enrollment,id=enrollment_id , student=request.user , status=Enrollment.Status.PENDING)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request,"Enrollment cancel succesfully")

    return redirect('my_enrollments')

    