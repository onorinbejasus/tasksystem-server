from django.conf.urls import url
from taskselection import views

urlpatterns = [
  url(r'^available_tasks/$', views.available_task_list)
]

