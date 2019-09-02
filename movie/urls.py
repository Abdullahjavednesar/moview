from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^/(?P<id>\d+)$', views.MovieView.as_view(), name="get"),
    re_path('^$', views.MovieView.as_view(), name="post"),
    re_path('^/(?P<id>\d+)$', views.MovieView.as_view(), name="delete"),
    re_path('^/actor/?$', views.ActorView.as_view(), name="getActor"),    
    re_path('^/actor/?(?P<id>\d+)$', views.ActorView.as_view(), name="getActor"),
    re_path('^/searchmoviebyactor/?$', views.searchMovieByActor, name="searchMovieByActor"),
    re_path('^/searchmovie/?$', views.searchMovie, name="searchMovie"),
    re_path('^/comment/?$', views.commentView),
    re_path('^/rating/?$', views.ratingView),
    re_path('^/addcast/?$', views.addCast),
    re_path('^/searchmoviebyrating/?$', views.searchMovieByRating),
    re_path('^/search/?$', views.search),


]