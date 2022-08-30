from django.db import models
from enum import auto, unique
from xml.etree.ElementTree import Comment
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

    def __str__(self) -> str:
        return self.message

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse(
            "posts:posts"
        )

    class Meta:
        ordering = ['-created_at']

class LikedPost(models.Model):
    user = models.ForeignKey(User, related_name='userlikes',on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.post.message + " liked by " + self.user.username



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=144)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)