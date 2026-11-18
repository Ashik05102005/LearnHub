from django.shortcuts import render,redirect
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


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
def home(request):
    return HttpResponse('Login succesfull')