from django import forms
from django.contrib.auth.models import User
from users.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Введите ваш логин',
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'password',
            'placeholder': 'Введите ваш пароль',
        })
    )


class SignupForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль',
            'id': 'password'
        })
    )
    confirm_password = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтвердите ваш пароль',
            'id': 'confirm_password'
        })
    )
    avatar = forms.ImageField(
        label="Загрузить аватарку",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'avatar',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя пользователя',
                'id': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вашу электронную почту',
                'id': 'email'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Пароли не совпадают')
        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый никнейм',
        })
    )

    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите новый email',
        })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    avatar = forms.ImageField(
        label="Изменить аватарку",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
        })
    )