# import fabrics API functions
from fabric.api import *

env.hosts = ['www-cartoterra@gueux.org:22']

def addcommit():
   local("git add -p && git commit")

def push():
   local("git push")

def prepare_deploy():
   #local("./manage.py test geodata")
   local("git add -p && git commit")
   local("git push")

def deploy():
   code_dir = '/srv/django/myproject'
   with cd(code_dir):
      run("git pull")
      run("touch wsgi.py")

def dev():
   """ Use development server settings """
   code_dir = '~/cartoterra/'
   with cd(code_dir):
      run("git pull")
      run("touch wsgi.py")

