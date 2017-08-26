from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    sv = self.context['request'].user
    tasks = Task.objects.filter(sv=sv)
    serializer = TaskSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

class SelectTask(APIView):
  def put(self, request, pk):
    sv = self.context['request'].user
    task = Task.objects.get(pk=pk)
    if task.sv == None:
      task.sv = sv
      task.save()
      serializer = TaskSerializer(task)
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response("task taken", status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk):
    sv = self.context['request'].user
    task = Task.objects.get(pk=pk)
    if task.sv == sv:
      task.sv = None
      task.save()
      serializer = TaskSerializer(task)
      return JsonResponse(serializer.data, safe=False)
    else:
      return Response("not our task", status=status.HTTP_400_BAD_REQUEST)

