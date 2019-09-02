from django.contrib import admin
from .models import Movie, Actor, ActMovRel, Comment, Rating


# Register your models here.
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(ActMovRel)
admin.site.register(Comment)
admin.site.register(Rating)
