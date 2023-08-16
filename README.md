# capitol_cinema_booking
Django monolithic app to handle movie reservations.
This app allows users to make reservations for screening shows.

![Arh](https://github.com/Cubillosxy/capitol_cinema_booking/blob/main/docs/app_arch.png)


 - Documentation generate with redoc [READ THE DOCS](/redoc/)
 - API DOCS [swagger](/api-doc/)
 - Project docs [notion](https://zenith-tuck-513.notion.site/Naya-Homes-Challenge-b428bedf28934d51bd9cfb8c38153253)
 - Arquitecture Diagram [monolith](https://github.com/Cubillosxy/capitol_cinema_booking/blob/main/docs/app_arch.png)


### Getting started local environment

* create ´.env´ by running ´ cp .env_example .env´
* set environment variables as required (DJANGO_SECRET_KEY: required)

* install pre-commit by running ´pip install pre-commit´
* run ´pre-commit install´

### Working flow 

* create new Branch from devel `git checkout -b mybranch` 
* push you branch and see the CI worlkflow [github-actions](https://github.com/Cubillosxy/capitol_cinema_booking/actions)
* open a new pull request to devel 
* check the workflow in [github-actions](https://github.com/Cubillosxy/capitol_cinema_booking/actions) to check QA deployment 


#### Running the development environment

* run ´docker-compose up --build´
* runing test ´docker exec -it capitol_cinema_booking-web-1 pytest´
     

### Hostnames for accessing the service directly
We provide pre-load-data for testing the service (only for testing purposes).

 * super user admin *admin@admin.com* password=admin
 * cinema owner user *owner@owner.com* password=owner
 * Local: http://127.0.0.1:8000
    - use swagger to test endpoints 
    - when you create a sreening the seats will be created
 


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
