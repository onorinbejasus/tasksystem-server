
# SV task selection system server

This is the code for the server part of the IEEE vis student volunteer task
selection system. The frontend code is at
https://github.com/VisSV/tasksystem-frontend.  The server is built using the
[Django REST framework](http://www.django-rest-framework.org). It's designed to
be deployed as a [Heroku app](http://heroku.com) but can really be run from
anywhere.

The task selection system uses websockets to transmit when people accept and
remove tasks so that other users logged into the selection system can get live
updates about what tasks are available.

## Installation

The system uses Python's virtual environment and pip to manage dependencies.
Everything was written using Python >3.5 so the code may not work with 
Python 2. 

Once you've checked out the repo then run the following commands to get your
developemnt environment set up:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This should download and instal the proper versions of all required packages.

## Local server

You can start the server in development mode. This will also start the
websocket server. When starting the server you need to specify which server
configuration to use.  There are 2 different configurations: development and
production. These configuration files are located at
`tasksystem/settings/dev.py` and `tasksystem/settings/prod.py` for the
development and production settings respectively. Development is primarily for
local development. It uses a local sqlite database. The production settings 
are set up for Heroku right now but these are intended for the "live" server.

To run the server in development mode:

```
python manage.py runserver --settings=tasksystem.settings.dev
```

or the local server in production mode:

```
python manage.py runserver --settings=tasksystem.settings.prod
```

Note that production mode will use the production database so be careful about
accidentally changing people's tasks!

### Configuration

If you open up one of the configuration files (or the `base.py` file they use)
there are alot of configuration variables. Most of these don't need to be 
changed. Some configuration parameters are easier as environmental variables
in Heroku so that's why they reference these. Key configuration parameters
are described below

#### `DEBUG`

If true, sets Django to debug mode which means you get a stack trace on error
sent to the client. You probably don't want this enabled on production 
systems.

#### `LOCK_TASKSELECTION`

Makes all tasks act like the `is_sticky` field is set to true. We set this
variable to "true" after the task selection period ends when we want the SVs 
to be able to view what tasks they selectd but not change them.

#### `SECRET_KEY`

This is used by Django for encrypting passwords and such. You can hard-code
this for developemnent but on production systems it should be kept secret so
that's why it's stored as an environment variable in production.

#### `DATABASES`

Contains the connection information. Heroku likes to put this in an 
environment variable.

#### `CORS_*`

Sets how permissive the server is about cross-origin scripts. For production
this is limited to things from vissv.org since we don't want people scripting
the interface to select tasks faster. There's a rate limiter too that helps
with this.

## Migrating the database

The database structure is controlled through Django's migrations feature.
This will update a database structure (or create it from scratch) that the
application needs. You can run the migrations with

```
python manage.py migrate --settings=<settings file>
```

## Loading data

There's some scripts to load both users and tasks into the system.

### Users

Create a csv file with the following columns of data:

* username
* firstname
* lastname
* password

For passwords you can use, e.g. http://random.org. I usually use the email
address as the username.

To load the users run:

```
python manage.py create_users --settings=<settings file> <csv file>
```

The creation script also takes a `--clear` option which will delete the users
from the database before loading in the new ones.

### Tasks

Create a csv file with the following columns:

* code
* category
* desc
* location
* date
* starttime
* endtime
* duration
* username

The username column can be blank. It allows you to assign a task to a specific
SV. This will pre-assign them to that task and mark it as "sticky" which 
keeps the task from getting dropped or assigned to anyone else. This is useful
for assigning day captains for instance.

```
python manage.py create_tasks --settings=<settings file> <csv file>
```

The creation script also takes a `--clear` option which will delete the tasks
from the database before loading in the new ones.

## Exporting information

Exporting information from the database is also done through the `manage.py`
script.

### Sign-in sheets

Creates the sign-in sheets to keep track of SV attendence during the 
conference.  This will create a .tex file for each day of tasks which can
be compiled with LaTeX.

```
python manage.py print_signin_forms --settings=<settings file> <export dir>
```

### Individual task forms

Creates a task list for each SV. This will create a single .tex file where
each page has a table of all the tasks for one SV.

```
python manage.py print_schedules --settings=<settings file> <tex file>
```

### Full-export

Exports a full export of the tasks and which SVs are linked to them. Useful
to load into Tableau or Excel to look into staffing shortages, etc.

```
python manage.py export_tasks --settings=<settings file> <csv file>
```

## Getting set up on Heroku

Heroku is a web application hosting service. It has a free tier which gives
a database and single web application server. This seems to be plenty of
capacity for the number of SVs that use the system at once.

If you haven't used Heroku before, it's pretty easy. The strange thing is
that they do everything through git. Here are the steps for deploying the
application server on Heroku:

1.  Sign up with heroku
2.  Install the Herkoku CLI tools
3.  Create a new app named 'sv-task-system'. It is important for the ALLOWED_HOSTS variable.
4.  Log into the web interface. You should see your newly created app there.
    Click on it to go to the settings.
5.  Click on "configure add-ons"
6.  Create a postgres database add-on. The free tier is fine.
7.  Create a redis database add-on (needed for websockets). The free tier 
    is also fine.
8.  Run `heroku config:set SECRET_KEY=<something>` where <something> is a 
    random string.
9. Run `git push heroku master` which will push your code to heroku, migrate
    the database, and start the server.
10. Run `heroku config:set LOCK_TASKS=false` this will ensure that tasks are
    not locked so SVs can select them.

You can check if the application is running by trying to access the root URL
of the server. This should give you a message that the server is running.
The root URL can be found in the settings page for your app.

Once the conference is over, it's probably a good idea to run the task export
script, save it somewhere, and then delete the app.

