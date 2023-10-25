from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone', 'avatar', 'country',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class VarificationForm(forms.Form):
    code = forms.CharField(max_length=4, min_length=4)


class RestorePasswordForm(forms.Form):
    email = forms.EmailField(max_length=150)
