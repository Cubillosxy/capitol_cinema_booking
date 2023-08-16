# capitol_cinema_booking
Django monolithic app to handle movie reservations.
This app allows users to make reservations for screening shows.


### Getting started local environment

- create ´.env´ by running ´ cp .env_example .env´
- set environment variables as required (DJANGO_SECRET_KEY: required)

- install pre-commit by running ´pip install pre-commit´
- run ´pre-commit install´


 ## Running the development environment
- run ´docker-compose up --build´
- runing test ´docker exec -it capitol_cinema_booking-web-1 pytest´
     

### Hostnames for accessing the service directly
We provide pre-load-data for testing the service (only for testing purposes).




#### Run tests and install libraries
docker exec -it capitol_cinema_booking-web-1 pytest -s
docker exec -it capitol_cinema_booking-web-1 pip install ipdb 

## Database commands

dump:

    docker exec capitol_cinema_booking-db-1 bash -c 'pg_dump --dbname=postgres --username=postgres > /tmp/data/db.dump'

restore:

    docker exec capitol_cinema_booking-db-1 bash -c 'psql --dbname=postgres --username=postgres --command="DROP SCHEMA public CASCADE;CREATE SCHEMA public;" && pg_restore /tmp/data/db.dump --dbname=postgres --username=postgres --no-owner'
    
    # restore with psql
    docker exec -it capitol_cinema_booking-db-1 bash -c 'psql postgres --username=postgres < /tmp/data/db.dump'

You can connect to the database shell using:

    docker exec -it capitol_cinema_booking-db-1 psql --dbname=postgres --username=postgres


To run any other command on the app container:
    docker exec -it capitol_cinema_booking-web-1 python manage.py makemigrations
    docker exec -it capitol_cinema_booking-web-1 python manage.py createsuperuser
    docker exec -it capitol_cinema_booking-web-1 python manage.py shell_plus
    docker exec -it capitol_cinema_booking-web-1 bash
