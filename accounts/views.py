from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

user = get_user_model()
# Create your views here.
def login_view(request):
    return render(request , 'login.html')

def register_view(request):
    print(CustomUserCreationForm())
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = CustomUserCreationForm()
    # print(form)
    return render(request,'register.html' , {'form' :form})

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password :
            messages.error(request,"Password do not match")
            return render(request,"forgot_password.html")

        try:
            user = User.objects.get(username=username)

            validate_password(password , user)
            user.set_password(password )
            user.save()
            messages.success(request , "Password updated successfully. Please log in")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request , "Invalid username.")
        except ValidationError as error :
            for message in error.messages :
                messages.error(request , message)
                
    return render(request , 'forgot_password.html')