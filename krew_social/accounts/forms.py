from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models
class NewUserForm(UserCreationForm):
    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        model = get_user_model()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label='username'
        self.fields['email'].label='Email Address'

# class UserProfileForm(forms.Form):
#     class Meta:
#         model = get_user_model()
#         fields = ['bio', 'pronouns']
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)

    