from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
  desc = models.TextField()
  location = models.TextField()
  code = models.IntegerField()
  date = models.DateField()
  starttime = models.TimeField()
  endtime = models.TimeField()
  is_sticky = models.BooleanField(default=False)
  sv = models.ForeignKey(User, null=True)

  @property
  def category(self):
    return int(self.code / 1000)

