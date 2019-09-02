from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, QueryDict, JsonResponse
from .models import Movie, Actor, Comment, Rating, ActMovRel
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

class MovieView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(MovieView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            name = request.POST['name']
            desc = request.POST['description']
            m = Movie(name=name, description=desc)
            m.save()
            return JsonResponse({'data': {'message': 'Movie saved successfully', 'id': m.id}})
        except:
            return JsonResponse({'error': {'message': 'Movie could not be saved'}})

    def get(self, request, id):
        try:
            m = Movie.objects.filter(id = id, exist=True).values("name", "description", "avg_rating", "actor")
            lst = list(m)
            if not lst == []:
                return JsonResponse({'data': lst})
            return JsonResponse({'error': {'message': "Movie not found", 'statusCode': '404'}}, status=404)
        except Exception as e:
            print (e)
            return JsonResponse({'error': {'message': "Bad request", 'statusCode': '400'}}, status=400)

    def delete(self, request, id):
        try:
            t = get_object_or_404(Movie, id=id)
            if not t.exist:
                return JsonResponse({'error': {'message': "Movie Not Found",'statusCode': '404'}},status=404)
            t.exist = False
            t.save()
            return JsonResponse({'data': {'message': 'Movie deleted'}})
        except:
            return JsonResponse({'error': {'message': "Movie Not Found",'statusCode': '404'}},status=404)

class ActorView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ActorView, self).dispatch(request, *args, **kwargs)

    def get(self, request, id):
        try:
            a = Actor.objects.get(id=id, exist=True)
            return JsonResponse({'data': {'Actor': a.name}})
        except:
            return JsonResponse({'error': {'message': "Actor Not Found",'statusCode': '404'}},status=404)

    def post(self, request):
        try:
            name = request.POST['name']
            a = Actor(name = name)
            a.save()
            return JsonResponse({'data': {'message': "Actor saved", 'id': a.id}})
        except:
            return JsonResponse({'error': {'message': "Bad request", 'statusCode': '400'}}, status=400)
    
    def delete(self, request, id):
        try:
            t = get_object_or_404(Actor, id=id)
            if not t.exist:
                return JsonResponse({'error': {'message': 'Actor not found', 'statusCode': '404'}},status=404)
            t.exist = False
            t.save()
            return JsonResponse({'data': {'message': 'Actor deleted'}})
        except:
            return JsonResponse({'error': {'message': 'Actor not found', 'statusCode': '404'}},status=404)

def addCast(request):
    m = Movie.objects.get(id = request.GET['movie_id'])
    a = Actor.objects.get(id = request.GET['actor_id'])
    role = request.GET['role']
    x = ActMovRel(movie = m, actor = a, role = role)
    x.save()
    m.actor.add(a)
    m.save()
    return JsonResponse({'data': {'Actor': a.name, 'Movie': m.name}})

def commentView(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'message': 'You are not logged in', 'statusCode': "401"}}, status=401)
    u = User.objects.get(id = request.user.id)
    movie = Movie.objects.get(id = request.GET['movie_id'])
    comment = request.GET['comment']
    c = Comment(user = u, comment = comment, movie = movie)
    c.save()
    return JsonResponse({'data': {'message': 'Successfully commented'}})

def ratingView(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'message': 'You are not logged in', 'statusCode': "401"}}, status=401)
    u = User.objects.get(id = request.user.id)
    movie = Movie.objects.get(id = request.GET['movie_id'])
    rating = int(request.GET['rating'])
    r = Rating(user = u, rating = rating, movie = movie)
    r.save()
    _ar = float(movie.avg_rating)
    tr = int(movie.total_rating)
    ar = (_ar * tr + rating) / (tr + 1)
    movie.total_rating += 1
    movie.avg_rating = ar
    movie.save()
    return JsonResponse({'data': {'message': 'Successfully rated'}})


def searchMovie(request):
    try:
        name = request.GET['name']
        m = Movie.objects.get(name = name, exist = True)
        if m.exist:
            star = ', '.join([str(i) for i in m.actor.all()])
            return JsonResponse({'data': {'Name': m.name, 'Description': m.description, 'Cast': star, 'Rating': m.avg_rating}})
        return JsonResponse({'error': {'message':'Movie not found', 'statusCode': '404'}}, status=404)
    except:
        return JsonResponse({'error': {'message':'Movie not found', 'statusCode': '404'}}, status=404)

def searchMovieByActor(request):
    try:
        name = request.GET['name']
        a = Actor.objects.get(name = name)
        mset = a.movie.filter(exist = True)
        movies = []
        for i in mset:
            movies.append(i.name)
        return JsonResponse({'data': {'Name': name, 'Movie': movies}})
    except:
        return JsonResponse({'error': {'message': "Bad request", 'statusCode': '400'}}, status=400)

def searchMovieByRating(request):
    try:
        gt = request.GET['rating_more_than']
        m = Movie.objects.filter(exist = True)
        mset=[]
        for i in m:
            if float(i.avg_rating) >= float(gt):
                mset.append(i.name)
        return JsonResponse({'data': {'Movies': mset}})
    except:
        return JsonResponse({'error': {'message': "Bad request", 'statusCode': '400'}}, status=400)

def search(request):
    try:
        try:
            name = request.GET['name']
        except:
            name = ""
        try:
            gt = request.GET['rating_more_than']
        except:
            gt = ""
        if not name == "" and not gt == "":
            actor_id = Actor.objects.get(name=name, exist=True)
            m = Movie.objects.filter(exist=True, actor=actor_id).values("name", "avg_rating")
            result = []
            for i in m:
                if float(i["avg_rating"]) >= float(gt):
                    result.append(i)
            return JsonResponse({'data': result})
        elif gt == "":
            a = Actor.objects.get(name = name, exist = True)
            mset = a.movie.all()
            movies = []
            for i in mset:
                movies.append(i.name)
            return JsonResponse({'data': {'Name': name, 'Movies': movies}})
        else:
            m = Movie.objects.filter(exist = True)
            mset=[]
            for i in m:
                if float(i.avg_rating) >= float(gt):
                    mset.append(i.name)
            return JsonResponse({'data': {'Movies': mset}})
    except:
        return JsonResponse({'error': {'message': "Bad request", 'statusCode': '400'}}, status=400)
