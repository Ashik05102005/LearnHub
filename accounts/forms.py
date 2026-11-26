from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta :
        model = CustomUser
        fields = [
            'username',
            'email',
            'phone',
            'address',
            'date_of_birth',
            'password1',
            'password2'
        ]

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    # used to remove help text
    # eg:Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None