from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class RegistrationForm(forms.ModelForm):
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Логин',
            'password': 'Пароль',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта',
        }
        widgets = {
            'password': forms.PasswordInput,
        }

    def save(self, commit=True):
        data = self.cleaned_data
        data.pop('password_confirm')
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)
        return user

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!', code='passwords_not_same')
        return password_confirm

    def clean_username(self):
        user = self.cleaned_data.get('username')
        try:
            User.objects.get(username=user)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Такой логин уже используется", code='login_in_use')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'about_me']