# Cartoterra project: Geolocalization of data related to earth building.

## Website

[https://cartoterra.net](https://cartoterra.net)

## License

See [COPYRIGHT](COPYRIGHT) file.

## Installation

### Development

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

#### Procedure

```shell
$ git clone https://git.gueux.org/cartoterra.git
Cloning into 'cartoterra'...
remote: Counting objects: 6296, done.
remote: Compressing objects: 100% (4469/4469), done.
remote: Total 6296 (delta 3539), reused 3267 (delta 1600)
Receiving objects: 100% (6296/6296), 7.13 MiB | 99.00 KiB/s, done.
Resolving deltas: 100% (3539/3539), done.
Checking connectivity... done.
$ virtualenv ~/cartoterra-env
$ source ~/cartoterra-env/bin/activate
(cartoterra-env)$ cd cartoterra
(cartoterra-env)$ cd grunt
(cartoterra-env)$ npm install
(cartoterra-env)$ grunt
(cartoterra-env)$ cd ..
(cartoterra-env)$ pip install -r ./requirements/base.txt
(cartoterra-env)$ pip install -r ./requirements/development.txt
(cartoterra-env)$ python manage.py migrate --settings=settings.development
(cartoterra-env)$ python manage.py createsuperuser --settings=settings.development
(cartoterra-env)$ python manage.py runserver --settings=settings.development
```

## Author

Félix Sipma [felix.sipma@no-log.org](mailto:felix.sipma@no-log.org)
