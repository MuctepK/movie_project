from django import forms
from django.contrib.auth.models import User

from accounts.models import Profile


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    password_confirm = forms.CharField(label="Подтвердите пароль", widget=forms.PasswordInput, strip=False)
    first_name = forms.CharField(label ='Имя', required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='Почта', required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']

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

