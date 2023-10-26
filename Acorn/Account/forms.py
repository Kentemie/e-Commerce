from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordResetForm,
    SetPasswordForm,
)

from .models import UserModel, UserAddress



class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = UserModel
        fields = ('username', 'first_name', 'last_name', 'email')


    username = forms.CharField(
        label='Username', 
        min_length=4, 
        max_length=50, 
        help_text='Required'
    )
    
    email = forms.EmailField(
        max_length=100, 
        help_text='Required', 
        error_messages={
            'required': 'Sorry, you need an email.'
        }
    )

    password = forms.CharField(
        label='Enter your password', 
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Repeat password', 
        widget=forms.PasswordInput
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'GayLord69'
        })
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'Michael Jordan'
        })
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'Jennifer Lopez'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'noobloser@gmail.com', 
            'name': 'email', 
            'id': 'id_email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mb-3', 
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Repeat password'
        })

    def clean_username(self):
        username = self.cleaned_data['username'].lower()

        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password2(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return self.cleaned_data['password2']

    def clean_email(self):
        email = self.cleaned_data['email']

        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email, that one is already taken')
        return email



class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(
       attrs={
            'class': 'form-control mb-3', 
            'placeholder': 'Username', 
            'id': 'login-username'
        })
    )

    password = forms.CharField(widget=forms.PasswordInput(
       attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        })
    )



class UserEditForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'first_name', 'last_name')


    username = forms.CharField(
        label='Firstname', 
        min_length=4, 
        max_length=50, 
        widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 
                   'placeholder': 'Username', 
                   'id': 'form-username', 
                   'readonly': 'readonly'
            }
        )
    )

    first_name = forms.CharField(
        label='First name',
        min_length=4,
        max_length=50, 
        widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 
                   'placeholder': 'First name', 
                   'id': 'form-firstname'
            }
        )
    )
    
    last_name = forms.CharField(
        label='Last name', 
        min_length=4, 
        max_length=50,
        widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 
                   'placeholder': 'Last name', 
                   'id': 'form-lastname'
            }
        )
    )
    
    email = forms.EmailField(
        label='Account email (can not be changed)', 
        max_length=200, 
        widget=forms.TextInput(
           attrs={'class': 'form-control mb-3', 
                   'placeholder': 'email', 
                   'id': 'form-email', 
                   'readonly': 'readonly'
            }
        )
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True



class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(
        max_length=254, 
        widget=forms.TextInput(
           attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'Email', 
                'id': 'form-email'
            }
        )
    )


    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserModel.objects.filter(email=email)
        if not user:
            raise forms.ValidationError(
                'Sorry, we can not find that email address')
        return email



class PwdResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='New password', 
        widget=forms.PasswordInput(
           attrs={'class': 'form-control mb-3', 
                   'placeholder': 'New Password', 
                   'id': 'form-newpass'
            }
        )
    )

    new_password2 = forms.CharField(
        label='Repeat password', 
        widget=forms.PasswordInput(
           attrs={'class': 'form-control mb-3',
                   'placeholder': 'New Password', 
                   'id': 'form-new-pass2'
            }
        )
    )



class UserAddressForm(forms.ModelForm):
    
    class Meta:
        model = UserAddress
        fields = ["country", "city", "postal_code", "address_line_1", "address_line_2", "phone_number_1"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["country"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "Country"}
        )
        self.fields["city"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "City"}
        )
        self.fields["postal_code"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "Postal code"}
        )
        self.fields["address_line_1"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "1234 Main St"}
        )
        self.fields["address_line_2"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "Apartment or suite"}
        )
        self.fields["phone_number_1"].widget.attrs.update(
            {"class": "form-control account-form", "placeholder": "(555) 555-1234"}
        )
