# import fabrics API functions
from fabric.api import *

def prepare_deploy():
   #local("./manage.py test my_app")
   local("git add -p && git commit")

def deploy():
   env.hosts =
   code_dir = '/srv/django/myproject'
   with cd(code_dir):
      run("git pull")
      run("touch app.wsgi")

def dev():
   """ Use development server settings """
   env.hosts = ['www-cartoterra@gueux.org']
   env['dir'] = '~/cartoterra/'
   code_dir = '~/cartoterra/'
   with cd(code_dir):
      run("git pull")
      run("touch wsgi.py")

