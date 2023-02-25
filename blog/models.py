from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    # title VARCHAR(255)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'pk': self.pk})


    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(default='Здесь будет описание статьи', verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    # blank=True - можно не вводить данные, null=True - может быть пустой в базе
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')  # Автоматом возьмет время создания
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')  # Автоматом возьмет время обновления статьи
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    # category_id INTEGER REFERENCES categories(category_id)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')


    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://images.wallpaperscraft.ru/image/single/mashina_seryj_mokryj_147750_3840x2160.jpg'


    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


# Создать модель Comment
# Которая знает Статью Пользователя Текст и Дату
# Создать форму для заполнения текста
# Улучшить Детали Статьи чтобы выводить форму, только если зарегестрировать
# Прописать вьюшку для сохранения комментария
# Доработать детали статьи для вывода комментариев
# Сделать куски HTML для вывода формы и комментариев


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ПОльзователь')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    def __str__(self):
        return f'{self.user.username} - {self.article} - {self.created_at}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='photos/users/', blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True, verbose_name='О себе')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Ссылка')

    def __str__(self):
        return self.user.username

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://freesvg.org/img/abstract-user-flat-4.png'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'