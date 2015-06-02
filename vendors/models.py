from datetime import timedelta

from django.db import models
from django.utils import timezone, encoding, decorators
# Create your models here.

class Vendor(models.Model):
  vehicle = models.CharField(max_length=50)
  name = models.CharField(max_length=100)
  url = models.CharField(max_length=200)
  food = models.CharField(max_length=100)
  img = models.CharField(max_length=200)

  def __str__(self):
    return '%s %s %s %s %s' % (self.name, self.vehicle, self.url, self.img, self.food)


class Event(models.Model):
  start_time = models.DateTimeField('event starts')
  end_time = models.DateTimeField('event ends')
  location = models.CharField(max_length=200) # may have to split up this field
  name = models.CharField(max_length=50)
  facebook_id = models.CharField(max_length=50)
  vendors = models.ManyToManyField(Vendor)

  def __str__(self):
    return '%s %s %s' % (self.location, self.name, self.facebook_id)
