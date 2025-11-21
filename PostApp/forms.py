from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title', 'content']


class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content', 'reply']
    widgets = {
      'reply': forms.HiddenInput() # Hide the reply field from the user interface
    }

"""
reply is optional, hidden in the form.

When a user clicks “reply” to a comment, you set the reply field in the view before saving.
"""