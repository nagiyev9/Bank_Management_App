from django import forms
from datetime import date
import re

MALE = 'M'
FEMALE = 'F'

GENDER_CHOICES = [
    (MALE, 'Male'),
    (FEMALE, 'Female'),
]

# Signup Form
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="First Name")
    last_name = forms.CharField(max_length=50, label="Last Name")
    username = forms.CharField(min_length=5, max_length=50, label="Username")
    email = forms.EmailField(
        min_length=9,
        label="Email",
        help_text="Please enter a valid email address."
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    number = forms.CharField(
        min_length=9,
        max_length=25,
        label="Phone Number",
        help_text="Example: +11234567890"
    )
    birthday_date = forms.DateField(
        label="Birthday Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="You must be at least 18 years old to register."
    )

    password = forms.CharField(
        min_length=8,
        label="Password",
        widget=forms.PasswordInput,
        help_text="Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character."
    )
    confirm = forms.CharField(
        min_length=8,
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    # Password Validation
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    # Password Confirmation Validation
    def clean_confirm(self):
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')
        if password != confirm:
            raise forms.ValidationError("Password and Confirm Password do not match.")
        return confirm

    # Age Validation (from Birthday Date)
    def clean_birthday_date(self):
        birthday_date = self.cleaned_data.get("birthday_date")
        if not birthday_date:
            raise forms.ValidationError("This field is required.")
        today = date.today()
        age = today.year - birthday_date.year - ((today.month, today.day) < (birthday_date.month, birthday_date.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birthday_date

# Login Form
class LoginForm(forms.Form):
    usernameOrEmail = forms.CharField(label="Username or Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# Confirmation Form Via Email
class ConfirmationCodeViaEmail(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label="Confirmation Code", help_text="Please enter the confirmation code sent to your email.")

# Confirmation Form Via Phone
class ConfirmationCodeViaPhone(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label="Confirmation Code", help_text="Please enter the confirmation code sent to your phone number.")

