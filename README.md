# Open city sign-ups

## Development with Docker

1. Create `.env` environment file

2. Set the `DEBUG` environment variable to `1`

3. Run `docker-compose up`

4. Run migrations if needed: 
    * `docker exec signups-backend python manage.py migrate`

5. Create superuser if needed: 
    * `docker exec -it signups-backend python manage.py createsuperuser`
   
6. Run the server:
    * `docker exec -it signups-backend python manage.py runserver 0:8000`


## Development without Docker

### Install pip-tools

* Run `pip install pip-tools`

### Creating Python requirements files

* Run `pip-compile requirements.in`
* Run `pip-compile requirements-dev.in`

### Updating Python requirements files

* Run `pip-compile --upgrade requirements.in`
* Run `pip-compile --upgrade requirements-dev.in`

### Installing Python requirements

* Run `pip-sync requirements.txt requirements-dev.in`

### Database

To setup a database compatible with default database settings:

Create user and database

    sudo -u postgres createuser -P -R -S open_city_signups  # use password `open_city_signups`
    sudo -u postgres createdb -O open_city_signups open_city_signups

Allow user to create test database

    sudo -u postgres psql -c "ALTER USER open_city_signups CREATEDB;"

### Daily running

* Set the `DEBUG` environment variable to `1`.
* Run `python manage.py migrate`
* Run `python manage.py runserver 0:8000`

## Running tests

* Set the `DEBUG` environment variable to `1`.
* Run `pytest`.
