from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import sys
import csv

User = get_user_model()

class Command(BaseCommand):
  help = 'Creates new users in the db for the given csv file'

  def add_arguments(self, parser):
    parser.add_argument('users', type=str)

  def handle(self, *args, **options):
    with open(options['users'], 'r') as csvfile:
      csvreader = csv.reader(csvfile, delimiter=';')
      # if this doesn't work the delimiter might be wrong
      for email, fname, lname, pw in csvreader:
        try:
          user = User.objects.create_user(username=email, email=email, 
                                          first_name=fname, last_name=lname)
          user.set_password(pw)
          user.save()

          assert authenticate(username=email, password=pw)
          self.stdout.write("User {0} successfully created.".format(email))
        except:
          print('There was a problem creating the user: {0}.  Error: {1}.' \
                .format(email, sys.exc_info()[1]))



