from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import TrackedItem, AppUser


class RegistrationForm(UserCreationForm):
    """Form class used to register new users
    """
    
    class Meta:
        model = AppUser
        fields = ["full_name", "email", "password1", "password2"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                    "placeholder": "Nom Prenom",
                    "class": "form-control",
                }),
            "email": forms.TextInput(attrs={
                    "placeholder": "Adresse email",
                    "class": "form-control",
                }),
        }
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': "Mot de passe",
            "class": "form-control",
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Mot de passe',
            'class': 'form-control',}
        )


class AddTrackedItem(forms.ModelForm):
    """class representing the form for adding a product to the tracked items
    """

    class Meta:
        """class helps configuring the AddTrackedItem ModelForm in relation to the TrackedItem model
        """

        model = TrackedItem
        fields = ('url', 'target_price', 'store')