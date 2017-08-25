from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
  name = models.TextField()
  code = models.IntegerField()
  starttime = models.DateTimeField()
  endtime = models.DateTimeField()
  sv = models.ForeignKey(User)

