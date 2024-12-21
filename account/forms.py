from django import forms
from datetime import datetime
import re

# Set Password Form
class CardPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=4,
        min_length=4,
        label='Card password',
        help_text='The password must contain digits only',
        widget=forms.PasswordInput
    )
    confirm = forms.CharField(
        max_length=4,
        min_length=4,
        label='Confirm password',
        widget=forms.PasswordInput
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain only number")
        if re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain only number")
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain only number")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain only number")
        if len(password) != 4:
            raise forms.ValidationError("Password length must be equal 4")
        
        return password
        
    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if password and confirm and password != confirm:
            raise forms.ValidationError("Password does not match")
        
        return password

# Deposit Amount Form
class SetDepositAmount(forms.Form):
    amount = forms.CharField(
        max_length=4,
        label="Amount",
        help_text="The amount should be between 1$ and 1000$",
        widget=forms.NumberInput(attrs={'min': 1,
        'max': 1000})
    )

# Deposit Card Form
class SetDepostCard(forms.Form):
    name_on_card = forms.CharField(
        min_length=5,
        label="Name on card",
        widget=forms.TextInput(attrs={
            'placeholder': 'John Doe',
            'class': 'form-control'
        }),
        required=True
    )
    card_number = forms.CharField(
        min_length=16,
        max_length=19,
        label="Card number",
        widget=forms.NumberInput(attrs={
            'min': 4155734600000000,
            'max': 4255734699999999,
            'placeholder': '0000 0000 0000 0000',
            'class': 'form-control'
        }),
        required=True
    )
    cvv = forms.CharField(
        min_length=3,
        max_length=3,
        label="CVV",
        widget=forms.NumberInput(attrs={
            'min': 100,
            'max': 999,
            'placeholder': '000',
            'class': 'form-control'
        }),
        required=True
    )
    expiry_date_month = forms.CharField(
        max_length=2,
        min_length=1,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'max': 12,
            'placeholder': 'MM',
            'class': 'form-control'
        })
    )
    expiry_date_year = forms.CharField(
        max_length=2,
        min_length=2,
        widget=forms.NumberInput(attrs={
            'min': datetime.now().year - 2000,
            'placeholder': 'YY',
            'class': 'form-control'
        })
    )
    expiry_date = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    street_adress = forms.CharField(
        label="Street Address",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    city = forms.CharField(
        label="City",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    state = forms.CharField(
        label="State/Province",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    zip_code = forms.CharField(
        label="Zip/Postal Code",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('expiry_date_month')
        year = cleaned_data.get('expiry_date_year')

        if month and year:
            try:
                expiry_date = datetime.strptime(f"{month}/{year}", "%m/%y")
                if expiry_date < datetime.now():
                    self.add_error('expiry_date_month', "Card has expired.")
                    self.add_error('expiry_date_year', "Card has expired.")
            except ValueError:
                self.add_error('expiry_date_month', "Invalid date format.")
                self.add_error('expiry_date_year', "Invalid date format.")

        return cleaned_data

# Search User By Username
class SearchUserForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username", help_text="Enter user username to who you want to send money", widget=forms.TextInput(attrs={'class': 'form-control border-2'}))    

# Send Money Form
class SendMoneyForm(forms.Form):
    amount = forms.CharField(
        max_length=4,
        label="Amount",
        help_text="The amount should be between 1$ and 1000$",
        widget=forms.NumberInput(attrs={
            'class': 'form-control border-2',
            'min': 1,
            'max': 1000
        })
    )

# Transfer Money To Bank Card Form
class TransferMoneyToBankCardForm(forms.Form):
    amount = forms.CharField(
        max_length=5,
        label="Amount",
        help_text="The amount should be between 1$ and 10000$",
        widget=forms.NumberInput(attrs={
            'class': 'form-control border-2',
            'min': 1,
            'max': 10000
        })
    )
    card_number = forms.CharField(
        min_length=16,
        max_length=16,
        label="Card number",
        widget=forms.NumberInput(attrs={
            'placeholder': '0000 0000 0000 0000',
            'class': 'form-control border-2'
        }),
        required=True
    )