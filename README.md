# Telephone API

Telephone is an application that provides an API to manage telephone calls.
It receives telephone call registries with the state of a call, like, start or stop, timestamp, and others.
Also, the application consolidate these registries into a call and charge them.

## Summary
1. [Requirements](#requirements)
    1. [Python Version and Environment](#python-version-and-environment)
    2. [Database and Queue](#database-and-queue)
    3. [O.S. and Hardware](#os-and-hardware)

2. [Installing and Running](#installing-and-running)
    1. [Heroku](#heroku)
    2. [Docker](#docker)
    3. [Running on bare metal](#bare-metal)

3. [Documentation](#documentation)
    1. [API Documentation](#api-documentation)
    2. [Dev Environment](#dev-environment)
    3. [Tests](#tests)
    4. [Internals](#internals)
    5. [Tips](#tips)


## Requirements
### Python Version and Environment
Telephone was developed using Python 3.7.2 with Python 3.6 capabilities at last in mind. So,
the application should run on Python 3.6.x environments without troubles. If you're gonna use Python 3.6
remember to use the latest 3.6.x release(3.6.8 at the time of this writing).

I've used __pyenv__ to manage python versions, and __pipenv__ to manage virtual environments. Both could be
used together. __Pipenv__ can use __pyenv__ and make everything work automagicly.

Also, I've used a Django Starter Template from Heroku guys. It have some facilities to work with Django software
on Heroku instances.

### Database and Queue
Perhaps Telephone was developed thinking about vendors lock-in, Postgres was the best choice for
a database. It have special fields like JSONB which could make it work as Document Oriented Database
or NoSQL as well. Also, most cloud vendors have a Postgres versions of his own  to be used as a
Database-as-a-Service.
For queue, Redis seems a nice choice too. It have an amazing speed, could be used as cache as well, and
vendors also have their version of it as a service.

### O.S. and Hardware
I've developed Telephone on a Linux Machine running Fedora 30, but it is expected to run flawlessly on any
\*NIX compatible OS(even Windows 10). It could run well on a simple instance with at least 1GB of RAM
and 512MB for each additional queue worker.


## Installing and Running
### Heroku
Since Telephone was developed with Heroku in mind, of course ir runs without much effort.
Just clone the project to your machine and get into the directory:
```bash
git clone https://github.com/decko/work-at-olist-rq
cd work-at-olist-rq
```
(If you need any help on configuring Heroku, read their documetation
[here](https://devcenter.heroku.com/articles/getting-started-with-python))

Now, just login to your Heroku account and create a new instance:
```bash
heroku login
heroku create
```
Remember the URL Heroku is giving to you in this moment. We're gonna
need it later.

Add the RedisToGo Add-on:
```bash
heroku addons:create redistogo
```

Publish your application to Heroku:
```bash
git push heroku master
```

You still need to set some environment variables to make it work:
```bash
heroku config:set DEBUG=False SECRET_KEY=<any randon sequence 64-letter long at least>
```
You could find any Telephone environment variable on this documentation.

Make sure your instance is working with:
```bash
heroku ps:scale web=1
heroku ps:scale worker=1
```

At least:
```bash
heroku run python manage.py migrate
```

And now access your instance using the URL that Heroku gave to you.
You sould see the Telephone API documentation page.

### Docker
Docker is a great container solution that ease the work with running app and
all the requirements. Consult Docker and docker-compose documentation to get it up and running.

Telephone have one Dockerfile to build an image for the application and a
docker-compose.yml to orquestrate all the containers needed to run the application.

After clone the application, run it with:
```bash
docker-compose up -d
```
and it shoud be available at `http://localhost:5000/`.

### Bare Metal
To run it on bare metal you gonna need to configure:
* Python, at least 3.6.8 version, preferably 3.7.3.
* Postgres 10.
* Redis 3.2.12 or the latest release for 3.2 branch.

I strongly recommend you to use __pipenv__ to manage the virtual
environment and dependencies. It do some magics that __pip__ still
can't. You can install __pipenv__ using __pip__ itself:
```bash
pip install -U pipenv
```

To create virtualenv and install dependencies, inside cloned application run:
```bash
pipenv install
```
(If you have you use pyenv along with pipenv, the last will ask you to install
the recommended Python version. ;))

Consult the documentation of your OS to install Postgres and Redis.
On Fedora you could easily go with:
```bash
sudo dnf install postgresql-server redis
```

Remember to configure __settings.py__ with the credentials for Postgres and Redis,
or set the DATABASE_URL and REDISTOGO_URL and other environment variables.
Now, your could run it with:
```bash
pipenv run honcho start web worker
```
and access it on `http://localhost:5000/`

## Documentation
### API Documentation
You can find the documentation after turn up an instance and accessing the URL. It's on root
URL. ;)
Also you can access `/docs` and `/redoc` which are diferent versions for the same documentation.

### Dev Environment
I've developed Telephone using [Neovim](https://neovim.io), on [Kitty](https://sw.kovidgoyal.net/kitty/)
terminal using tmux and zsh with prezto.
You can find my configuration files [here](https://gitlab/decko/dotfiles).
I've used to develop on two machines, a Lenovo T470 Laptop and a Ryzen7 Desktop, both with 16GB of RAM.
Used docker to run Postgres and Redis, and executed the code inside a pipenv virtual environment.

### Tests
To run the tests you must build up a virtualenv and install development dependencies.
```bash
pipenv install --dev
pipenv run pytest --create-db
```
and it should run all the tests.

### Internals
The application is developed around a Service concept. A Service is a subclass of
ServiceAbstractClass with a trigger and queue attributes. Every time a message is
sent with `dispatch`, a Service is triggered, instantiated with a message.
A message could be anything, since a complete json set, an id, or other.
Then, a sequence of functions runs to obtain, validate, transform, persist and
propagate information to a queue, where a new trigger is fired and the process goes on.

So, if you want to build a service you need to subclass ServiceAbstractClass and explicity create
all methods needed to make it run. Set a trigger attribute and a queue one. The queue is where the
result or anything you want goes after the process is done.

### Tips
You could easily use Docker to run __Postgres__ and __Redis__ containers.
To run Postgres:
```bash
docker run -d -p 5432:5432 -e POSTGRES_DB=telephonedb -e POSTGRES_USER=olist_telephone -e POSTGRES_PASSWORD=olist_telephone --name olist-pgdb postgres:10
```

and Redis:
```bash
docker run -d -p 6379:6379/tcp --name olist-redis redis:3-alpine
```

And, you could use [__podman__](https://podman.io) which runs Docker images
as normal users, without user scalation.
