from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'comments']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your name (optional)',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email (optional)',
                'class': 'form-input'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comments': forms.Textarea(attrs={
                'placeholder': 'Share your experience with us...',
                'rows': 5,
                'class': 'form-textarea'
            }),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'rating': 'Rating',
            'comments': 'Comments'
        }