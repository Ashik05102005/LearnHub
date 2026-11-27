from django import forms
from .models import Courses
from django.conf import settings
from django.contrib.auth import get_user_model
# create Forms 

User = get_user_model()

class CourseForm(forms.ModelForm):

    class Meta :
        model = Courses
        fields = ['title','description','instructor']

    def __init__(self, *args , **kwargs):

        user = kwargs.pop('user', None)

        super().__init__(*args , **kwargs)

        self.fields['instructor'].queryset = User.objects.filter(groups__name='Instructor').distinct()

        self.fields['instructor'].label = 'Select Instructor'

        if user and user.groups.filter(name='Instructor').exists():
            self.fields.pop('instructor')
