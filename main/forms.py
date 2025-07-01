from django import forms
from .models import Comment, Contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']    


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Messages'}),
        }
