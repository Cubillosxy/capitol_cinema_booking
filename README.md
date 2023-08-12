# capitol_cinema_booking
Django monolith app to handle movie reservation 


### Getting started local environment

- create ´.env´ by running ´ cp .env_example .env´
- create ´local_settings´ by run ´cp local_settings.example.py capitol_cinema/local_settings.py´

- run ´pre-commit install´
 ## other commands 

     
## Database

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
