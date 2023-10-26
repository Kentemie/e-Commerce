from django import forms
from django.contrib.auth import get_user_model

from .models import PaymentSelections



class PaymentSelectionsForm(forms.ModelForm):

    class Meta:
        model = PaymentSelections
        fields = ["name",]

    
    name = forms.ChoiceField(
        choices=PaymentSelections.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )



class UserForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


    username = forms.CharField(
        label='Username', 
        min_length=4, 
        max_length=50, 
        help_text='Required',
        widget=forms.TextInput
    )
    
    email = forms.EmailField(
        max_length=100, 
        help_text='Required', 
        error_messages={
            'required': 'Sorry, you need an email.'
        }
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'id': 'username',
            'class': 'form-control', 
            'placeholder': 'GayLord69'
        })
        self.fields['first_name'].widget.attrs.update({
            'id': 'first_name',
            'class': 'form-control', 
            'placeholder': 'Michael Jordan'
        })
        self.fields['last_name'].widget.attrs.update({
            'id': 'last_name',
            'class': 'form-control', 
            'placeholder': 'Jennifer Lopez'
        })
        self.fields['email'].widget.attrs.update({
            'id': 'email',
            'class': 'form-control', 
            'placeholder': 'noobloser@gmail.com', 
            'name': 'email', 
        })

    def clean_email(self):
        user = self.instance
        email = self.cleaned_data.get('email')

        if email != user.email:
            raise forms.ValidationError("Email does not match your current email.")
        
        return email
    
    def clean_username(self):
        user = self.instance
        username = self.cleaned_data.get('username')

        if username != user.username:
            raise forms.ValidationError("Username does not match your current username.")
        
        return username