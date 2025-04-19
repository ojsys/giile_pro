from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'mdc-text-field__input', 'placeholder': 'Your Email'}),
            'content': forms.Textarea(attrs={'class': 'mdc-text-field__input', 'rows': 5, 'placeholder': 'Your Comment'}),
        }