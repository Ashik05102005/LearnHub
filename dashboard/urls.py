"""
URL configuration for LearnHub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path 
from . import views

urlpatterns = [
    path('' , views.dashboard_redirect , name='dashboard_redirect'),
    path('admin_dashboard/',views.admin_View,name='admin_view'),
    path('instructor_dashboard/',views.instructor_View,name='instructor_view'),
    path('student_dashboard/',views.student_View,name='student_view'),
    path('user_list/' , views.user_list , name = 'user_list') , 
]
