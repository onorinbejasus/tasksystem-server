from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from taskselection.models import Task
from taskselection.serializers import TaskSerializer
from rest_framework.views import APIView

class AvailableTaskList(APIView):
  def get(self, request):
    tasks = Task.objects.filter(sv=None)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

class SelectedTaskList(APIView):
  def get(self, request):
    # FIXME: authentication and search by user
    #sv = request.user
    sv = User.objects.get(pk=1)
    tasks = Task.objects.filter(sv=sv)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

class SelectTask(APIView):
  def put(self, request, code):
    #sv = request.user
    sv = User.objects.get(pk=1)
    task = Task.objects.get(code=code)
    if task.sv == None:
      task.sv = sv
      task.save()
      serializer = TaskSerializer(task)
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response("task taken", status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, code):
    #sv = request.user
    sv = User.objects.get(pk=1)
    task = Task.objects.get(code=code)
    if task.sv == sv:
      task.sv = None
      task.save()
      serializer = TaskSerializer(task)
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response("not our task", status=status.HTTP_400_BAD_REQUEST)

