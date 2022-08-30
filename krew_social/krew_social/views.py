from django.views.generic import TemplateView
from django.urls import reverse_lazy

class HomePage(TemplateView):
    template_name = 'index.html'

