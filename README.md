# Cartoterra project: Geolocalization of data related to earth building.

## Website

[https://cartoterra.net](https://cartoterra.net)

## License

See [COPYRIGHT](COPYRIGHT) file.

## Installation

### Development

#### Requirements

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
$ virtualenv ~/cartoterra-env
$ source ~/cartoterra-env/bin/activate
(cartoterra-env)$ cd /path/to/your/cartoterra/repo
(cartoterra-env)$ cd grunt
(cartoterra-env)$ npm install
(cartoterra-env)$ grunt
(cartoterra-env)$ cd ..
(cartoterra-env)$ pip install -r ./requirements/production.txt
(cartoterra-env)$ pip install -r ./requirements/development.txt
(cartoterra-env)$ spatialite cartoterra.db "SELECT InitSpatialMetaData();"
(cartoterra-env)$ python manage.py syncdb --noinput --settings=settings.development
(cartoterra-env)$ python manage.py migrate --settings=settings.development
(cartoterra-env)$ python manage.py createsuperuser --settings=settings.development
(cartoterra-env)$ python manage.py runserver --settings=settings.development
```

## Author

Félix Sipma [felix.sipma@no-log.org](mailto:felix.sipma@no-log.org)
