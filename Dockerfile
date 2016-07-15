FROM buildpack-deps:stretch
RUN apt-get update
RUN apt-get install -y python-pip npm python-pyspatialite libspatialite-dev libsqlite3-mod-spatialite
RUN mkdir /code
WORKDIR /code
ADD requirements/base.txt /code/
ADD requirements/development.txt /code/
RUN pip install -r development.txt
ADD grunt /code/grunt
WORKDIR /code/grunt
RUN npm install
## TODO: remove ln -s ...?
## /usr/bin/env: node: No such file or directory
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN /code/grunt/node_modules/.bin/grunt
WORKDIR /code
ENV DJANGO_SETTINGS_MODULE settings.development
