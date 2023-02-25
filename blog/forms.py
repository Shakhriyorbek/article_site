from django import forms
from .models import Article, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'photo', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Напишите название статьи'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Напишите содержимое статьи'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select selectpicker bg-dark text-light'
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Ваш комментарий'
            })
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'link', 'photo']

        widgets = {
            'bio': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Расскажите о себе (255 символов)'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Ссылка на вашу соц сеть'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light',
            })
        }

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Ваш юзер'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Ваше имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Ваша фамилия'
            }),
        }