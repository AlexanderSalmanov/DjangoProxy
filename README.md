# DjangoProxy

Django-based project which allows creating `Site` objects pointing to real-world websites. <br>
Once connected to the external site, all its internal navigation is altered so that the user navigates within the application, but not in the external website. <br>
If the user clicks on an external route - the application redirects him/her to the original external URL route.

## Tech stack
- Python
- Django
- PostgreSQL
- BeautifulSoup4
- Docker
- HTML/CSS/jQuery/Bootstrap v5.1.3

## Prerequisites
- Docker installed on your local machine

## Local installation steps

1. `git clone` the repository to the desired directory.
2. Create the `.env` file at the same location as `.env.example`. Copy the contents of `.env.example` to `.env`.
3. Build the project with `docker-compose build`.
4. Run the project in docker with `docker-compose up`.
5. Run the database migrations with `docker-compose exec api python manage.py migrate`. Make sure that both `api` and `db` containers are running!
6. Create a superuser with `docker-compose exec api python manage.py createsuperuser` (Optional) 
7. Navigate to `localhost:8000` in your browser and test the application!
