# Foodgram
```
Реквизиты для проверки развернутой на сервере работы:

сайт: https://antoncp.hopto.org/
IP: 158.160.21.122

Суперпользователь (с доступом в админку):
email: admin@gmail.com
username: admin
password: adminpas57

Еще один тестовый пользователь:
email: antoncp@gmail.com
username: antoncp
password: testpas57 
``` 
### Description
What happens when you cross Instagram and your love of food - you get Foodgram. Here you can share photos and descriptions of your favorite recipes, check out others, subscribe to talented chefs and follow their suggestions. Over 2000 ingredients for a wide variety of dishes are already listed in our database.  

This service is based on modern, fast and secure technologies: React on the frontend side and Django REST Framework as the backend REST API.  
 
### Technologies
`Python 3.9`
`Django 3.2`
`Django REST framework`
`Djoser`
`React 17.0.1`
`Docker`

### How to launch project on local machine with Docker 
- Clone the repository
```
git clone git@github.com:antoncp/foodgram-project-react.git
``` 
- In project root folder call a Docker compose up command
```
docker compose up
``` 
- Make database migrations in the started backend container
```
docker compose exec backend python manage.py migrate
``` 
- Collect static files for Django admin panel
```
docker compose exec backend python manage.py collectstatic
``` 
- Copy these files to the target folder, connected with Docker volume
```
docker compose exec backend cp -r /app/collected_static/. /foodgram_static/
``` 

### How to launch only backend in a dev-mode without Docker
- Create and activate virtual environment
```
python3.9 -m venv venv
``` 
- Install dependencies from requirements.txt file with activated virtual environment
```
pip install -r requirements.txt
``` 
- In folder with file manage.py make migrations
```
python manage.py migrate
``` 
- Populate the database with prepared ingredients in a .csv-file
```
python manage.py load_csv foodgram_static/ingredients.csv Ingredient
```
- And execute a command to run a server
```
python manage.py runserver
```

### How to launch project on web-server with Docker 
- Clone to the target folder on server `docker-compose.production.yml` file and create your own `.env` file (similar to the .env.example file in this repository). Also clone the `infra` folder with the `nginx.conf` settings.

- In project root folder call a Docker compose up command, specified the file to the `docker-compose.production.yml`
```
sudo docker compose -f docker-compose.production.yml up -d
``` 
- Repeat the migrate and collect static steps from the local launch above.
### Examples of using REST API
You could find detailed roadmap of using REST API of this project in [docs/openapi-schema.yml](https://github.com/antoncp/foodgram-project-react/blob/master/docs/openapi-schema.yml). Or you can examine it directly on site [antoncp.hopto.org/redoc/](https://antoncp.hopto.org/redoc/).

### Authors
Yandex Practicum, Anton Chaplygin

