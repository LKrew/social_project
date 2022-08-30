from random import choices
from tkinter import CASCADE
from django.contrib import auth
from django.db import models
from django.contrib.auth import get_user_model

U = get_user_model()
# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return "@{}".format(self.username)

class UserProfile(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'
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

