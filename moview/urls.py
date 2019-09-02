from django.contrib import admin
from django.urls import path, re_path, include

from .views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies', include('movie.urls')),
    path('', home),
    path('users/', include('accounts.urls')),
]
