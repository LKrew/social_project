from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from . import forms
from . import models
from django.shortcuts import redirect
# Create your views here.

class NewUser(CreateView):
    model = forms.NewUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/new_user.html'

class UpdateProfile(UpdateView):
    
    #template_name = 'accounts/edit_profile.html'
    model = models.UserProfile
    fields = ['bio', 'pronouns']
   
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        form.instance.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('posts:profile', kwargs={'username':self.request.user})