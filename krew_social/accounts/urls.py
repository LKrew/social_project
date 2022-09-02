from django.urls import re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'login/', auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    re_path(r'logout/',auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'signup/',views.NewUser.as_view(), name='signup'),
    re_path(r'edit_profile/(?P<pk>\d+)/', views.UpdateProfile.as_view(), name='edit_profile'),
    re_path(r'follow/(?P<pk>\d+)/', views.follow_user, name='follow_user'),
]