from django import forms
from .models import Farmer


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = [
            'name',
            'mobile',
            'email',
            'village',
            'district',
            'state',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter farmer name'
            }),

            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),

            'village': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter village'
            }),

            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),

            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
        }