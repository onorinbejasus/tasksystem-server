from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from taskselection.models import Task
import sys
from os import path
import csv

User = get_user_model()

EXPORT_FIELDS = [
  'code',
  'desc',
  'starttime',
  'endtime',
  'firstname',
  'lastname'
]

PREAMBLE = """
\\documentclass[12pt]{article}

\\usepackage[landscape,margin=0.5in]{geometry}
\\usepackage{longtable}

\\begin{document}

\\section*{%s}

\\renewcommand\\arraystretch{2.1}
\\begin{center}
\\begin{longtable}{%s}
\\hline
%s \\\\
\\hline
\\endhead
"""

POSTAMBLE = """
\\hline
\\end{longtable}
\\end{center}
\\end{document}
"""

def sanitize_latex(s):
  return s.replace("&", "\\&")

def format_head(date, fields):
  frmt = "|" + "|".join("l"*len(fields))
  frmt = frmt + "|p{10em}|p{10em}|"
  flds = ["\\textbf{%s}" % (f) for f in fields + ["sign-in", "sign-out"]]
  flds = " & ".join(flds)
  return PREAMBLE % (str(date), frmt, flds)

def format_line(task):
  row = [task.code, task.desc, task.starttime, task.endtime]
  if task.sv:
    row = row + [task.sv.first_name, task.sv.last_name]
  else:
    row = row + ["", ""]
  row = row + ["", ""] # sign in/out fields
  row = [str(f) for f in row]
  row = [sanitize_latex(f) for f in row]
  return " & ".join(row) + " \\\\"

class Command(BaseCommand):
  help = 'Prints the signin forms for each day'

  def add_arguments(self, parser):
    parser.add_argument('export_dir', type=str)

  def handle(self, *args, **options):
    task_dates = Task.objects.order_by('date').values('date').distinct()
    for td in task_dates:
      d = td['date'] # FIXME: messy
      tasks = Task.objects.filter(date=d).order_by('starttime')
      print(d.strftime("%m%d"))
      texfile = path.join(options['export_dir'], d.strftime("%m%d") + ".tex")
      # print a tex file with a table for each day
      with open(texfile, "w") as output:
        print(format_head(d, EXPORT_FIELDS), file=output)
        for task in tasks:
          print(format_line(task), file=output)
          print("\\hline", file=output)
        print(POSTAMBLE, file=output)


