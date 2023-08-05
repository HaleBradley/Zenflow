from django import forms

class SignupForm(forms.Form):
    first_name = forms.CharField(label='first_name')
    last_name = forms.CharField(label='last_name')
    birth_date = forms.CharField(label='birth_date')
    phone_number = forms.CharField(label='phone_number')
    email = forms.CharField(label='email')
    password = forms.CharField(label='password')
    confirm_password = forms.CharField(label='confirm_password')
    team_id = forms.CharField(label='team_id', required=False)

class LoginForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='password')