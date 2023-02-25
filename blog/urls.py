from django.urls import path
from .views import *

urlpatterns = [
    # path('', index, name='index'),
    # path('category/<int:pk>/', category_view, name='category'),
    # path('article/<int:pk>/', article_view, name='article'),
    # path('add_article/', add_article, name='add_article')
    path('', ArticleList.as_view(), name='index'),
    path('category/<int:pk>/', ArticleListByCategory.as_view(), name='category'),
    path('article/<int:pk>/', ArticleDetail.as_view(), name='article'),
    path('add_article/', NewArticle.as_view(), name='add_article'),
    path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='delete'),

    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),

    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('profile/<int:pk>', profile_view, name='profile'),
    path('profile/<int:pk>/edit/', edit_profile_view, name='edit_profile'),
    path('user/<int:pk>/edit/', edit_user_view, name='edit_user')
]
