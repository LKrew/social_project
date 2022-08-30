from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from . import forms
from . import models
# Create your views here.

class NewUser(CreateView):
    form_class = forms.NewUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/new_user.html'

class UpdateProfile(FormView):
    template_name = 'accounts/edit_profile.html'
    form_class = forms.UserProfileForm
    success_url = reverse_lazy('posts:profile',{'username':'user.username'})