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

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    country_code = forms.CharField(max_length=5, initial='+251')  # Set the default country code
    phone_number = forms.CharField(max_length=9)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
