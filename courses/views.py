from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from .form import CourseForm
from .models import Courses
from django.contrib import messages

# Create your views here.
@login_required
@permission_required('courses.add_courses' , raise_exception=True)
def create_course(request) :

    is_admin = request.user.groups.filter(name='Admin').exists()

    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            if not is_admin:
                course.instructor = request.user
            course.save()

        return redirect('course_list')
    
    else :
        form = CourseForm()

    return render(request , 'create_course.html',{'form':form})

@login_required
def course_list(request):

    if request.user.groups.filter(name='Admin').exists() :
        courses = Courses.objects.all()

    elif request.user.groups.filter(name='Instructor').exists():
        courses = Courses.objects.filter(instructor=request.user)

    else :
        courses = Courses.objects.all()
    
    return render(request,'course_list.html',{'courses':courses})

@login_required
def course_details(request,course_id):
    
    course = get_object_or_404(Courses,id=course_id)

    is_admin = request.user.groups.filter(name = 'Admin').exists()

    is_instructor = request.user.groups.filter(name='Instructor').exists()

    can_manage_course = (is_admin or is_instructor and course.instructor == request.user)

    return render(request,'course_details.html',{'course':course , 'can_manage_course' : can_manage_course })

@login_required
def edit_course(request , course_id):
    course = get_object_or_404(Courses,id=course_id)
    is_admin = request.user.groups.filter(name='Admin').exists()

    if not is_admin and course.instructor != request.user :
        return HttpResponse("Permission Denied", status=403)
    
    if request.method == "POST":
        form = CourseForm(request.POST , instance=course)

        if form.is_valid():
            form.save()
            return redirect('course_details',course_id=course.id)
        
    else:
        form = CourseForm(instance=course)

    return render(request,'edit_course.html',{'form':form , 'course' : course})

@login_required
def delete_course(request , course_id):
    course = get_object_or_404(Courses , id = course_id)
    is_admin = request.user.groups.filter(name='Admin').exists()

    if not is_admin and course.instructor != request.user :
        return HttpResponse("Permission Denied", status=403)

    if request.method == 'POST' :
        course.delete()
        messages.success(request,'Course deleted successfully')
        return redirect('course_list')
    
    return render(request,'delete_course.html',{'course':course})

    

