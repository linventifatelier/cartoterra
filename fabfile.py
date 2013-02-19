# import fabrics API functions
from fabric.api import *
import os


#env.hosts = ['www-cartoterra@gueux.org']
if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
    env.use_ssh_config = True
env.hosts = ['felix@panterre-local']
env.disable_known_hosts = True

env.app_user = "www-cartoterra"
env.base_dir = '/srv/cartoterra'
env.code_dir = env.base_dir + "/src"
env.virtualenv = env.base_dir + '/cartoterra-env'
env.gunicorn_pid = env.base_dir + '/gunicorn-cartoterra.pid'

def test():
   with settings(warn_only=True):
      result = local('python manage.py test geodata', capture=True)
   if result.failed and not confirm("Tests failed. Continue anyway?"):
      abort("Aborting at user request.")


def sudo_virtualenv(command, **kwargs):
    sudo("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def pull():
    sudo("git pull", user="%s" % env.app_user)

def collectstatic():
    sudo_virtualenv("python manage.py collectstatic --noinput", user=env.app_user)


def reload_gunicorn():
    sudo("kill -HUP $(cat %s)" % env.gunicorn_pid, user=env.app_user)


def update_app():
    with cd(env.code_dir):
        pull()
        collectstatic()

def deploy():
    update_app()
    reload_gunicorn()

