# Cartoterra project: Geolocalization of data related to earth building.

## Website

[https://cartoterra.net](https://cartoterra.net)

## License

See [COPYRIGHT](COPYRIGHT) file.

## Development

### Git

You have to use git to get the latest versions of cartoterra.net. To know more about git:
https://git-scm.com/doc

cartoterra.net has a git repo:
https://gitweb.gueux.org/?p=cartoterra.git;a=summary

cartoterra.net dev version is available on Github:
https://github.com/linventifatelier/cartoterra.git

• install git
https://git-scm.com/doc)https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

• create + configure a local repo
- create a folder on your computer to host all cartoterra.net files
- open terminal and go to your folder (e.g. $ cd /Documents/web/cartoterraFolder )

```shell
$ git init 
```

• pull cartoterra.net into it

```shell
$ git clone https://git.gueux.org/cartoterra.git 
Cloning into 'cartoterra'...
remote: Counting objects: 6296, done.
remote: Compressing objects: 100% (4469/4469), done.
remote: Total 6296 (delta 3539), reused 3267 (delta 1600)
Receiving objects: 100% (6296/6296), 7.13 MiB | 99.00 KiB/s, done.
Resolving deltas: 100% (3539/3539), done.
Checking connectivity... done.
```

up-to-date files should be uploaded to your folder.

### Recommended method: docker

Install dockera and docker-compose:
https://www.docker.com/products/overview#/install_the_platform

run (and get a coffee while docker is building the container and attaching to it):

```shell
$ docker-compose build
...
$ docker-compose up
...
Starting src_web_1
Attaching to src_web_1
```

go to:
http://127.0.0.1:8000 in your browser, modify files in the repo and reload the page to see your modifications.


### Manual method

#### Requirements

- git
- python2.7
- virtualenv
- pip
- GEOS
- GDAL
- PROJ.4
- spatialite
- libsqlite3-mod-spatialite
- npm

If you don’t know about python, pip and virtualenv:
http://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/

#### Manual installation on a Mac OSX

It is highly recommended to use homebrew (http://brew.sh/)

##### Install Python 2.7

Python 2.7 is installed with the system on Mac. You shouldn’t have anything to do.
You can install an updated version of python with homebrew (won't change your system version):
$ brew install python

if you need, python download page:
https://www.python.org/downloads/

##### Install pip

```shell
$ sudo easy_install pip 
```

##### Install virtualenv

```shell
$ sudo pip install virtualenv 
```

##### Install geos, gdal, proj.4, spatialite (for MAC)

```shell
$ brew update
$ brew install spatialite-tools
$ brew install gdal
```

Alternative solution for systems up to Mavericks:
• Go to http://www.kyngchaos.com/software:frameworks
• download and install « GDAL Complete »

##### Install npm

```shell
$ brew install node
```

##### Create virtualenv and install cartoterra.net requirements

```shell
$ virtualenv ~/cartoterra-env
$ cd cartoterra
$ source ~/cartoterra-env/bin/activate
(cartoterra-env)$ cd grunt
(cartoterra-env)$ npm install
(cartoterra-env)$ grunt
(cartoterra-env)$ cd ..
(cartoterra-env)$ pip install -r ./requirements/development.txt
(cartoterra-env)$ python manage.py migrate --settings=settings.development
(cartoterra-env)$ python manage.py createsuperuser --settings=settings.development
(cartoterra-env)$ python manage.py runserver --settings=settings.development
```


#### Procedure

After you have followed the previous steps, to update cartoterra.net and launch your local server (repeat each time you want to start a server session):
```shell
$ git pull https://git.gueux.org/cartoterra.git
$ cd cartoterra
$ source ~/cartoterra-env/bin/activate
(cartoterra-env)$ cd grunt
(cartoterra-env)$ npm install
(cartoterra-env)$ grunt
(cartoterra-env)$ cd ..
(cartoterra-env)$ pip install -r ./requirements/development.txt
(cartoterra-env)$ python manage.py migrate --settings=settings.development
(cartoterra-env)$ python manage.py runserver --settings=settings.development
```

## Import/Export

Massive import/export is possible in the administration interface for the
following models:

- Building
- Worksite
- Event
- Stakeholder

`geometry` column must use one of the syntax:

- `LON,LAT` (for example `40,40`) for default `SRID` (`4326`)
- `SRID:LON,LAT` (for example `4326:40,40`) to specify a different `SRID`

The following columns can take multiple values (separated by ","):

- Building:
    - techniques
    - stakeholder
    - groups
- Worksite
    - techniques
    - stakeholder
    - groups
- Event
    - techniques
    - stakeholder
    - type_of_stakeholders
    - groups
- Stakeholder
    - techniques
    - role
    - groups

References to external models are specified with the name of the related entry. The following columns use references to external models:

- Building
    - techniques
    - stakeholder
    - groups
    - creator
    - classification
    - use
    - property_status
    - earth_quantity
    - protection_status
    - heritage_status
- Worksite
    - techniques
    - stakeholder
    - groups
    - creator
- Event
    - techniques
    - stakeholder
    - type_of_stakeholders
    - groups
    - creator
    - event_type
- Stakeholder
    - techniques
    - role
    - groups
    - creator


## Authors

Félix Sipma [felix.sipma@@no-log.org](mailto:felix.sipma@@no-log.org)
Grégoire Paccoud [gregoire.paccoud@@gmail.com](gregoire.paccoud@@gmail.com)
