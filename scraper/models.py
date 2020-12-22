from django.db import models

class School(models.Model):
    name = models.CharField(max_length=20)
    total_population = models.IntegerField(default=200)
    date_of_establishment = models.DateField()
    is_private = models.BooleanField(default=False)