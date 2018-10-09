from tasksystem.settings.base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Option to lock down the task system
if os.environ.get('LOCK_TASKS', 'false').lower() == 'true':
  LOCK_TASKSELECTION = True
else:
  LOCK_TASKSELECTION = False

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'] = db_from_env

ALLOWED_HOSTS = ['sv-task-server.herokuapp.com']

# websockets
CHANNEL_LAYERS['default'] = {
  "BACKEND": "asgi_redis.RedisChannelLayer",
  "CONFIG": {
    "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
  },
  "ROUTING": "taskselection.routing.channel_routing",
}

#SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY = '12345abc'

# CORS settings
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
  'vissv.org'
)
CORS_REPLACE_HTTPS_REFERER = True
CORS_ALLOW_CREDENTIALS = True

