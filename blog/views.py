from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Article, Category, Comment, Profile
from .forms import ArticleForm, LoginForm, RegistrationForm, CommentForm, ProfileForm, EditUserForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from django.contrib import messages


# Create your views here.


# def index(request):
#     articles = Article.objects.all()
#     context = {
#         'title': 'Главная страница PROWEB-БЛОГ',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)


class ArticleList(ListView):  # article_list.html
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'  # По умолчанию ответ вернет - objects
    extra_context = {'title': 'Главная страница PROWEB-БЛОГ'}


    def get_queryset(self):
        articles = Article.objects.annotate(comments_count=Count('comment')).all()
        return articles

# def category_view(request, pk): # pk - primary key - id категории
#     category = Category.objects.get(pk=pk)
#     articles = Article.objects.filter(category=category)
#     context = {
#         'title': f'Категория: {category.title}',
#         'articles': articles
#     }
#     return render(request, 'blog/index.html', context)


class ArticleListByCategory(ArticleList):

    def get_queryset(self):
        articles = Article.objects.filter(category_id=self.kwargs['pk'])
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Категория: {category.title}'
        return context


# def article_view(request, pk): # id - статьи
#     article = Article.objects.get(pk=pk)
#
#     context = {
#         'title': f'Статья: {article.title}',
#         'article': article
#     }
#
#     return render(request, 'blog/article_detail.html', context)


class ArticleDetail(DetailView):  # article_detail.html
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        article = Article.objects.get(pk=self.kwargs['pk'])
        article.views += 1
        article.save()
        context['title'] = f'Статья: {article.title}'
        context['comments'] = Comment.objects.filter(article=article)
        context['comments_count'] = len(Comment.objects.filter(article=article))
        articles = Article.objects.all()
        articles = articles.order_by('-views')
        context['articles'] = articles[:4]

        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return context


# def add_article(request):
#     if request.method == 'POST':
#         form = ArticleForm(request.POST, request.FILES)
#         if form.is_valid():
#             # form.cleaned_data # В виде словаря {'title': 'Заголовок'....}
#             article = Article.objects.create(**form.cleaned_data)
#             article.save()
#             return redirect('article', article.pk)
#     else:
#         form = ArticleForm()
#
#     context = {
#         'title': 'Создание статьи',
#         'form': form
#     }
#     return render(request, 'blog/article_form.html', context)


# GET POST не надо - класс сделает все сам
class NewArticle(CreateView):
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {'title': 'Создание статьи'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    extra_context = {'title': 'Изменение статьи'}


class ArticleDelete(DeleteView):
    model = Article
    context_object_name = 'article'
    success_url = reverse_lazy('index')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('index')
        else:
            messages.error(request, 'Не верные логин/пароль')
            return redirect('login')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт')
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')



def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта')
    return redirect('index')


def save_comment(request, pk):  # pk - id статьи
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = Article.objects.get(pk=pk)
        comment.save()
    return redirect('article', pk)



def profile_view(request, pk): # pk - id пользователя
    profile = Profile.objects.get(user_id=pk)
    articles = Article.objects.filter(author_id=pk)
    context = {
        'profile': profile,
        'articles': articles
    }
    return render(request, 'blog/profile.html', context)


def edit_profile_view(request, pk):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
        return redirect('profile', pk)

    else:
        form = ProfileForm(instance=Profile.objects.get(user_id=pk))

        context = {
            'form': form
        }
        return render(request, 'blog/edit_profile.html', context)


def edit_user_view(request, pk):
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
        return redirect('profile', pk)

    else:
        form = EditUserForm(instance=request.user)

        context = {
            'form': form
        }
        return render(request, 'blog/edit_profile.html', context)



