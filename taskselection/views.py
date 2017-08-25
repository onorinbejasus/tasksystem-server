from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taskselection.models import Task
from taskselection.serializers import TaskSerializer

def available_task_list(request):
  if request.method == 'GET':
    tasks = Task.objects.filter(sv=None)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

