from django import forms
from .models import ContactResponse

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactResponse
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'new-name'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'new-email'}),
            'message': forms.Textarea(attrs={'autocomplete': 'new-message'}),
        }