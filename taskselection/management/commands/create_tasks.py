from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import authenticate
from taskselection.models import Task
import sys
import csv

class Command(BaseCommand):
  help = 'Creates new tasks in the db for the given csv file'

  def add_arguments(self, parser):
    parser.add_argument('tasks', type=str)

  def handle(self, *args, **options):
    with open(options['tasks'], 'r') as csvfile:
      csvreader = csv.DictReader(csvfile, delimiter=';')
      # if this doesn't work the delimiter might be wrong
      for row in csvreader:
        print(row)
        try:
          task = Task.objects.create(
            desc = row['desc'],
            location = row['location'],
            code = row['code'],
            starttime = row['starttime'],
            endtime = row['endtime'],
            date = row['date'],
          )
          task.save()

          self.stdout.write("Task {0} successfully created.".format(row['code']))
        except:
          print('There was a problem creating the task: {0}.  Error: {1}.' \
                .format(row['code'], sys.exc_info()[1]))



