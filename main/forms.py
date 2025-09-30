from django import forms

class ContactForm(forms.Form):
    fullname = forms.CharField(
        max_length=100,
        required=True,   # <-- Asl joyi shu
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Full name',
            'data-form-input': True
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email Address',
            'data-form-input': True
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Your Message',
            'rows': 5,
            'data-form-input': True
        })
    )
