from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskselection.models import Task
import sys
import csv

User = get_user_model()

TRUE_VALS = [
  'true',
  '1',
  't',
]
def parse_truth(v):
  return v.lower() in TRUE_VALS

class Command(BaseCommand):
  help = 'Creates new tasks in the db for the given csv file'

  def add_arguments(self, parser):
    parser.add_argument('tasks', type=str)
    parser.add_argument('--clear', dest='clear_tasks', default=False, action='store_true')

  def handle(self, *args, **options):
    if options['clear_tasks']:
      ans = input('Setting --clear will delete all tasks from the database. Is this ok? (Y/N) ')
      if ans =='Y':
        print('Deleting all tasks')
        Task.objects.all().delete()
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
            #is_sticky = parse_truth(row['sticky'])
          )
          task.save()

          self.stdout.write("Task {0} successfully created.".format(row['code']))

          # see if we should bind this task to a particular user
          if row['username']:
            sv = User.objects.get(username=row['username'])
            if not sv:
              raise "User {0} not found".format(row['username'])
            task.sv = sv
            task.is_sticky = True
            task.save()
            self.stdout.write("Task {0} bound to {1}.".format(row['code'], row['username']))

        except:
          print('There was a problem creating the task: {0}.  Error: {1}.' \
                .format(row['code'], sys.exc_info()[1]))



