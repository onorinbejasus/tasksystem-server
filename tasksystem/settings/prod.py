from tasksystem.settings.base import *
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'] = db_from_env

# websockets
CHANNEL_LAYERS['default'] = {
  "BACKEND": "asgi_redis.RedisChannelLayer",
  "CONFIG": {
    "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
  },
  "ROUTING": "taskselection.routing.channel_routing",
}


