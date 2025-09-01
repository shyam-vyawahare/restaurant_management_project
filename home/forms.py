from django import forms
from .models import Feedback
from .models import ContactSubmission

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

# Contact form submission code here
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email Address',
                'class': 'form-input'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Your message (optional)',
                'rows': 4,
                'class': 'form-textarea'
            }),
        }
        labels = {
            'name': 'Name',
            'email': 'Email',
            'message': 'Message'
        }