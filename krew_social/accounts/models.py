from django.contrib import auth
from django.db import models
from django.contrib.auth import get_user_model

U = get_user_model()
# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)

class UserProfile(models.Model):
    MALE = 'he/him'
    FEMALE = 'she/her'
    NONBINARY = 'they/them'
    NONE = ''
    pronouns_choices = [
                        (MALE,'he/him'),
                        (FEMALE, 'she/her'),
                        (NONBINARY, 'they/them'),
                        (NONE, '')
                        ]
    user = models.OneToOneField(U, on_delete=models.CASCADE)
    bio = models.TextField(max_length=144)
    pronouns = models.CharField(max_length=9, choices=pronouns_choices, default='none')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    followers = models.ManyToManyField(User, related_name='followers',blank=True)
    
class Following(models.Model):
    user = models.ForeignKey(UserProfile, related_name='following_user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(UserProfile, related_name='followed', on_delete=models.CASCADE)

class Followers(models.Model):
    user = models.ForeignKey(UserProfile, related_name='followed_user', on_delete=models.CASCADE)
    following_user = models.ForeignKey(UserProfile, related_name='user_following', on_delete=models.CASCADE)
