from django.contrib.gis.db import models
from users.models import CustomUser


class Polygon(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.PolygonField()  # geo-json info
