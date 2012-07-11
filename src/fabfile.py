# import fabrics API functions
from fabric.api import *

env.hosts = ['www-cartoterra@gueux.org']
env.disable_known_hosts = True

env.virtualenv = 'cartoterra-env'
env.code_dir = 'cartoterra'
env.gunicorn_pid = 'gunicorn-cartoterra.pid'
env.requirements = env.code_dir + "/src/requirements/project.txt"
env.local_python = 'python2.6'

def add():
   local("git add -p")

def commit():
   local("git commit")

def push():
   local("git push")

def run_ls():
   run('ls -alt',  capture=False)

def init_remote():
   with cd(code_dir):
      run("git clone git@gueux.org:cartoterra.git .")
   run("virtualenv --distribute %s" % env.virtualenv_dir)
   run("source %s/bin/activate && pip install -r %s" %
       (env.virtualenv, env.requirements))
   run("ln -s /usr/lib/%(localpython)s/dist-packages/xapian/__init__.py \
       %(env)s/lib/%(localpython)s/site-packages/xapian.py && \
       ln -s %(env)s/lib/%(localpython)s/site-packages/xapian_backend.py \
       %(env)s/lib/%(localpython)s/site-packages/haystack/backends/" %
       { 'localpython': env.local_python, 'env': env.virtualenv,})



def prepare_deploy():
   #local("./manage.py test geodata")
   add()
   commit()
   push()

def deploy():
   with cd(env.code_dir):
      run("git pull")
      run("kill -HUP $(cat %s)" % env.gunicorn_pid)

