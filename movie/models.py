from django.db import models
from django.contrib.auth.models import User

class Actor(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank = True)
    age = models.PositiveIntegerField(blank = True)
    gender = models.CharField(max_length = 20, blank = True)
    exist = models.BooleanField(default=True)
    def __str__(self):
            return self.name
    def __repr__(self):
            return self.name

class Movie(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank = True)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default = 0)
    total_rating = models.IntegerField(default=0)
    actor = models.ManyToManyField(Actor, related_name='movie', through='ActMovRel', blank = True)
    exist = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ' - ' + str(self.avg_rating) + '/5'

class ActMovRel(models.Model):
    actor = models.ForeignKey(Actor, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    role = models.CharField(max_length=100)

class Comment(models.Model):
    comment = models.TextField(max_length=200)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)


class Rating(models.Model):
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)


###############################################################################
# User
#     - Registration
#     - Authentication
# Movie information
#     - Add movie details
#         - Image
#         - Name
#         - Description
#         - Cast
#             - Name
#             - Role
#             - Date of birth
#             - Age
# Rating
#     - Cumulative
#     - My own rating
# Search
#     - By movie name
# Search with filters
#     - By actor name
# Comment