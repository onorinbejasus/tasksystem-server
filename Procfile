release: python manage.py migrate --settings=tasksystem.settings.prod
web: daphne tasksystem.asgi:channel_layer --port=$PORT -v2
worker: python manage.py runworker -v2
