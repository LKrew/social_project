from .models import Comment, Repost
from django import forms
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

