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

from django.db import models

class Actor(models.Model):
     Name = models.CharField(max_length=100)

     def __str__(self):
         return self.Name

class movie(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=1000)
    Rating = models.DecimalField(max_digits=3, decimal_places=2)
    Stars = models.ManyToManyField(Actor, blank = True)

    def __str__(self):
        return self.Name + ' - ' + str(self.Rating) + '/5'

class cast(models.Model):
    Movies = models.ManyToManyField(movie, blank = True)
    Name = models.CharField(max_length=100)
    Role = models.CharField(max_length=100)
    Dob = models.DateField(null=True)
    Age = models.PositiveIntegerField()

    def __str__(self):
        return self.Name
