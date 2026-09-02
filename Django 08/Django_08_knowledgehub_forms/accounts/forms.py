from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Username",
        min_length=3,
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Username here'}),
    )
    email = forms.EmailField(label="Email",
                             widget=forms.TextInput(attrs={'placeholder': 'Email here'}),)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),)
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

class LoginForm(forms.Form):
    username_or_mail = forms.CharField(
        label="Username or mail",
        widget=forms.TextInput(attrs={'placeholder': 'Username or mail here'}),)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),)
