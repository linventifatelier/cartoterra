# import fabrics API functions
from fabric.api import *


env.hosts = ['www-cartoterra@gueux.org']
env.disable_known_hosts = True

env.virtualenv = '/home/www-cartoterra/cartoterra-env'
env.code_dir = '/home/www-cartoterra/cartoterra'
env.gunicorn_pid = 'gunicorn-cartoterra.pid'
env.src = env.code_dir + "/src"
env.requirements = env.src + "/requirements/project.txt"
env.local_python = 'python2.6'
env.local_postgis = '/usr/share/postgresql/9.1/contrib/postgis-1.5'

def test():
   with settings(warn_only=True):
      result = local('python manage.py test geodata', capture=True)
   if result.failed and not confirm("Tests failed. Continue anyway?"):
      abort("Aborting at user request.")

def init_local():
   local("sudo apt-get update && sudo apt-get install postgresql python-xapian \
   postgis postgresql-9.1-postgis gdal-bin libpq-dev proj-bin libgeos-dev \
   libgeos++-dev")
   local("sudo su -s postgres && createdb -E UTF8 template_postgis && \
   createlang -d template_postgis plpgsql && \
   psql -d postgres -c \"UPDATE pg_database SET datistemplate=\'true\' WHERE \
     datname=\'template_postgis\';\" &&\
   psql -d template_postgis -f %(localpostgis)/postgis.sql && \
   psql -d template_postgis -f %(localpostgis)/spatial_ref_sys.sql && \
   psql -d template_postgis -c \"GRANT ALL ON geometry_columns TO PUBLIC;\" && \
   psql -d template_postgis -c \"GRANT ALL ON spatial_ref_sys TO PUBLIC;\" && \
   psql -d template_postgis -c \"GRANT ALL ON geography_columns TO PUBLIC;\"" %
         { 'localpostgis': env.local_postgis })
   local("python manage.py syncdb")
   local("python manage.py convert_to_south profiles")
   local("python manage.py convert_to_south geodata")
   local("python manage.py migrate")

def pull()
   local("git pull")
   local("python manage.py syncdb")
   local("python manage.py migrate")

def add():
   local("git add -p")

def commit():
   local("git commit")

def push():
   local("git push")

def update_requirements():
   run("source %s/bin/activate && pip install -r %s" %
       (env.virtualenv, env.requirements))

def syncdb():
   run("cd %s && source %s/bin/activate && python manage.py syncdb && \
        python manage.py migrate" % (env.src, env.virtualenv))

def init_remote():
   with cd(env.code_dir):
      run("git clone git@gueux.org:cartoterra.git .")
   run("virtualenv --distribute %s" % env.virtualenv)
   update_requirements()
   run("ln -s /usr/lib/%(localpython)s/dist-packages/xapian/__init__.py \
          %(env)s/lib/%(localpython)s/site-packages/xapian.py && \
       ln -s %(env)s/lib/%(localpython)s/site-packages/xapian_backend.py \
          %(env)s/lib/%(localpython)s/site-packages/haystack/backends/ && \
       ln -s /usr/lib/%(localpython)s/dist-packages/xapian/_xapian.so \
          %(env)s/lib/%(localpython)s/site-packages/" %
       { 'localpython': env.local_python, 'env': env.virtualenv,})
   syncdb()

def prepare_deploy():
   #test()
   add()
   commit()
   push()


def deploy():
   with cd(env.code_dir):
      run("git pull")
      syncdb()
      run("kill -HUP $(cat %s)" % env.gunicorn_pid)


