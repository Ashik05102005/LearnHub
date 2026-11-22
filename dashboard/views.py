from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
@login_required
def dashboard_redirect(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('admin_view')
    elif user.groups.filter(name='Instructor').exists():
        return redirect('instructor_view')
    elif user.groups.filter(name='Student').exists():
        return redirect('student_view')
    else :
        return render(request,'unautherized_view.html',status=403)

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Admin').exists() , login_url='unauthorized_view')
def admin_View(request):
    return render(request ,'admin_dashboard.html')

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Instructor').exists() , login_url='unauthorized_view')
def instructor_View(request):
    return render(request ,'instructor_dashboard.html')

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Student').exists() , login_url='unauthorized_view')
def student_View(request):
    return render(request ,'student_dashboard.html')