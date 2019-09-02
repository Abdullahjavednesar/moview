from django.shortcuts import render
from django.http import HttpResponse, Http404, QueryDict
from .models import movie, cast, Actor
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator


class MovieView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MovieView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            name = request.POST['name']
            desc = request.POST['desc']
            rating = request.POST['rating']
            m = movie(Name = name, Description = desc, Rating = rating)
            m.save()
            return HttpResponse("movie saved")
        except:
            raise Http404("Couldn't Save :(")

    def get(self, request):
        try:
            id = request.GET['id']
            m = movie.objects.get(id=id)
            # star = ', '.join([str(i) for i in m.Stars.all()])
            return HttpResponse(m.Name)
        except:
            raise Http404("Bad request :(")
        
class ActorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ActorView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            id = request.GET['id']
            a = Actor.objects.get(id=id)
            return HttpResponse(a.Name)
        except:
            raise Http404("Actor Not Found :(")

    def post(self, request):
        try:
            name = request.POST['name']
            a = Actor(Name = name)
            a.save()
            return HttpResponse("actor saved")
        except:
            raise Http404("Actor couldn't be saved :(")

def searchMovie(request):
    try:
        name = request.GET['name']
        m = movie.objects.get(Name = name)
        star = ', '.join([str(i) for i in m.Stars.all()])
        return HttpResponse('Name: ' + m.Name + '\nDescription: ' + m.Description + '\nRating: ' + m.Rating + '\nStars: '+ star)
    except:
        raise Http404("Movie not found :(")

def searchMovieByActor(request):
    try:
        name = request.GET['name']
        a = cast.objects.filter(Name = name)
        movies = ""
        for j in range(0, a.count()):
            movies = movies + ', '.join([str(i) for i in a[j].Movies.all()])
        if movies != "":
            return HttpResponse('Movies of ' + name + ' are ' + movies)
        else:
            return HttpResponse("No movie available of Actor " + name)
    except:
        raise Http404("Bad Request :(")
