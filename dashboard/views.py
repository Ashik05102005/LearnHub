from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import get_user_model 
from courses.models import Courses
from django.contrib import messages
from django.contrib.auth.models import Group
from django.db.models import Q

User = get_user_model()

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
    context = {
        'total_users':User.objects.count() ,
        'total_students' :User.objects.filter(groups__name = 'Student').distinct().count(),
        'total_instructors' :User.objects.filter(groups__name = 'Instructor').distinct().count(),
        'total_courses' :Courses.objects.count()
    }
    return render(request ,'admin_dashboard.html',context)

@login_required
@user_passes_test(lambda user:user.groups.filter(name='Admin').exists() , login_url='unauthorized_view')
def user_list(request):
    users = User.objects.prefetch_related('groups').all().order_by('-id')
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group')

        user = get_object_or_404(User , id = user_id)

        if user.is_superuser:
            messages.error(request , "Superuser group cannot be changed here.")
            return redirect('user_list')

        group = get_object_or_404(
            Group,
            id = group_id ,
            name__in = ['Admin' , 'Instructor' , 'Student'] 
        )

        if user == request.user and group.name != 'Admin' :
            messages.error(request,"You cannot remove your own Admin access")
            return redirect('user_list')

        user.groups.set([group])

        messages.success(
            request , 
            f"{user.username} is now assigned to {group.name}"
        )
        return redirect('user_list')
    search = request.GET.get('search','')
    selected_group = request.GET.get('group','')

    if search :
        users = users.filter(
            Q(username_icontains = search) | Q(email_icontains = search)
        )

    if selected_group in ['Admin','Instructor','Student']:
        users = users.filter(groups__name = selected_group)

    context = {
        'users' : users.distinct(),
        'search' : search , 
        'selected_group' : selected_group , 
        'groups' : Group.objects.filter(
            name__in = ['Admin' , 'Instructor' , 'Student']
        )
    }
    
    return render(request , 'user_list.html',context)

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Instructor').exists() , login_url='unauthorized_view')
def instructor_View(request):
    return render(request ,'instructor_dashboard.html')

@login_required
@user_passes_test(lambda user: user.groups.filter(name='Student').exists() , login_url='unauthorized_view')
def student_View(request):
    return render(request ,'student_dashboard.html')