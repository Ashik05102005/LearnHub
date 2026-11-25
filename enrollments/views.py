from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
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

@login_required
@user_passes_test(lambda user : user.groups.filter(name='Instructor').exists())
def instructor_enrollments(request):
    if request.method == 'POST':
        enrollment_id = request.POST.get('enrollment_id')
        action = request.POST.get('action')

        enrollment = get_object_or_404(Enrollment , id = enrollment_id , course__instructor = request.user , status = 'Pending')

        if action == 'approve' :
            enrollment.status = 'Approved'
            enrollment.save(update_fields=['status'])
            messages.success(request , 'Enrollment approved successfully.')
        elif action == 'reject' :
            enrollment.status = 'Reject'
            enrollment.save(update_fields=['status'])
            messages.success(request , 'Enrollment rejected successfully.')
        return redirect('instructor_enrollments')
    
    enrollments = Enrollment.objects.filter(course__instructor = request.user ,
                                            status = 'Pending').select_related(
                                                'student' , 'course' , 'course__instructor').order_by('-id')
    return render(request , 'instructor_enrollment.html' , {'enrollments' : enrollments})
    

    