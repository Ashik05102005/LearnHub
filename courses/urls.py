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
    path('create_course/',views.create_course , name='create_course'),
    path('course_list/',views.course_list , name='course_list'),
    path('course_details/<int:course_id>/',views.course_details , name='course_details'),
    path('edit_course/<int:course_id>/',views.edit_course,name='edit_course'),
    path('delete_course/<int:course_id>',views.delete_course,name='delete_course')
]
