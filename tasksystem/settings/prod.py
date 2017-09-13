from tasksystem.settings.base import *

DEBUG = False

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'tasksystem',
  }
}


