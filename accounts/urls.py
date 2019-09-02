from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path('^register/?$', views.RegisterView.as_view(), name="post"),
    re_path('^login/?$', views.LoginView.as_view(), name="login"),
    re_path('^logout/?$', views.LogoutView.as_view(), name="logout"),
    re_path('^authenticate/?$', views.CheckAuthView.as_view(), name="authenticate"),
    re_path('^changepass/?$', views.ChangePasswordView.as_view(), name="changepass"),
]