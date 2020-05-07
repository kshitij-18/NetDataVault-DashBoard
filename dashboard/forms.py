from django import forms
from . models import User, Profile, AuthKeyModel
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    address = forms.CharField(widget=forms.Textarea)
    pin_code = forms.IntegerField(label='Pin Code')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': '',
            'password2': ''
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'pin_code')


class AuthKeyCollectForm(forms.ModelForm):
    class Meta:
        model = AuthKeyModel
        fields = ('auth_key',)


class AuthKeyVerifyForm(forms.Form):
    API_Key = forms.CharField(max_length=100)
