#from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
class locationDetail(models.Model):
    user = models.ForeignKey(User, on_delete= models.PROTECT,null = True, related_name="user_location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.PointField(null=False, blank=False, srid=4326, verbose_name="Location")
    last_fetched = models.DateTimeField(null = True)
    def __str__(self):
        return self.user.username + "'s location at "+ str(self.last_fetched)
# Create your models here.
