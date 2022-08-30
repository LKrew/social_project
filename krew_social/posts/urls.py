from django.urls import re_path
from posts import views

app_name = 'posts'

urlpatterns = [
    re_path(r'^post_list/$', views.PostList.as_view(), name='posts' ),
    re_path(r'^profile/(?P<username>[-\w]+)/$', views.UserPostList.as_view(), name='profile'),
    re_path(r'^createpost/$', views.NewPost.as_view(), name='new_post'),
    re_path(r'delete/(?P<pk>\d+)/$', views.DeletePost.as_view(), name='delete'),
    re_path(r'like/(?P<pk>\d+)/$', views.like_post, name='like'),
    re_path(r'unlike/(?P<pk>\d+)/$', views.unlike_post, name='unlike'),
    re_path(r'single/(?P<pk>\d+)/$', views.SinglePost.as_view(), name='single'),
]