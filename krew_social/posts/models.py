from django.db import models
from enum import auto, unique
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

User = get_user_model()

class Post(models.Model):
    message = models.TextField(max_length=144)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    comments_on_post = models.ForeignKey('posts.Comment', related_name='comments_on_post', on_delete=models.CASCADE, null=True)
    reposts = models.ForeignKey('posts.Repost', related_name='reposts', on_delete=models.CASCADE, null=True)
    is_post = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.message
    
    def get_absolute_url(self):
        return reverse(
            "posts:posts"
        )
    class Meta:
        ordering = ['-created_at']

class LikedPost(models.Model):
    author = models.ForeignKey(User, related_name='userlikes',on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post.message + " liked by " + self.user.username

class Repost(models.Model):
    post = models.ForeignKey(Post, related_name='repost', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='reposter', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_post = models.BooleanField(default=False)
    def __str__(self):
        return self.author.username + " reposted " + self.post.author.username + "'s post"
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='usercomment', on_delete=models.CASCADE)
    text = models.TextField(max_length=144)
    created_date = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='likes_comment', blank=True)

    def __str__(self):
        return self.text

class LikedComment(models.Model):
    author = models.ForeignKey(User, related_name='userlikescomment',on_delete=models.CASCADE)
    comment = models.ForeignKey('posts.Comment', on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.text + " liked by " + self.user.username