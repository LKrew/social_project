from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from . import forms
from .models import User, UserProfile, Followers, Following
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http  import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from itertools import chain

# Create your views here.
U = get_user_model()
class NewUser(CreateView):
    
    form_class = forms.NewUserForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/new_user.html'

class UpdateProfile(UpdateView):
    
    model = UserProfile
    fields = ['bio', 'pronouns']
   # form_class = forms.UserProfileForm
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        form.instance.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

    def get_success_url(self) -> str:
        return reverse('posts:profile', kwargs={'username':self.request.user.username})

@login_required
def follow_user(request, pk):
    if request.method == "POST":

        uwf = U.objects.get(pk=pk)

        user_who_was_followed = UserProfile.objects.get(user=request.user)

        user_who_followed = UserProfile.objects.get(user=uwf)

        following_table = Following(user=user_who_followed, followed_user=user_who_was_followed)

        follower_table = Followers(user=user_who_was_followed, following_user=user_who_followed)
        #adds user to Post 
        user_who_was_followed.followers.add(user_who_followed.user.id)
        user_who_followed.following.add(user_who_was_followed.user.id)
        

        user_who_was_followed.save()
        user_who_followed.save()
        following_table.save()
        follower_table.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))