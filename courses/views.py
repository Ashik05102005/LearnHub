from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required , permission_required
from .form import CourseForm
from .models import Courses

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
