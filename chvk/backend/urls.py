from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='Sign up'),
    path('signin/', views.sign_in, name='Sign in'),
    path('refresh/', views.refresh, name='Refresh tokens'),
    path('getmovies/', views.get_movies, name='Get movies'),
    path('topupbalance/', views.top_up_balance, name='Top up balance'),
    path('subscription/', views.subscription, name='Subscription'),
    path('bought/', views.bought_movies, name='Get bought movies'),
    path('review/', views.review, name='Review'),
    path('revs/', views.movie_revs, name='Refs about movie'),
]