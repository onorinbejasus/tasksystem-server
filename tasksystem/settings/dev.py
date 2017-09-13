from tasksystem.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p#$hm-6n0^c6f6iuf0^iu0sla_()$)gt196m=cz&6_48_=68yq'

CHANNEL_LAYERS['default'] = {
  "BACKEND": "asgiref.inmemory.ChannelLayer",
  "ROUTING": "taskselection.routing.channel_routing",
}

