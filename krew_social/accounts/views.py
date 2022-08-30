from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
# Create your views here.

class NewUser(CreateView):
    form_class = forms.NewUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/new_user.html'