# Blog project

## Notes

### Features
On top of basic CRUD functionality, this web app has several other features:
1. Mobile first, mobile and web responsive
2. 

### To run locally
1. pip install -r requirements.txt --no-index
- pip freeze > requirements.txt

### To deploy
- git commit heroku master
- heroku run python manage.py migrate
- heroku open

### To open virtual environment
- export PYTHONPATH="/Users/huishun/Desktop/project"
- virtualenv env
- source env/bin/activate

### To migrate
- python manage.py makemigrations
- python manage.py migrate

### To set up postgres locally
1. lunchy start postgres
2. psql postgres -U huishun
3. psql postgres (cntr-d to quit)
4. lunchy stop postgres

### To make virtual environment
- python3 -m venv env

### To add env variabes
- heroku config:get CONFIG-VAR-NAME -s  >> .env


### Create database
- createdb blog_code
- dropdb blog_code

## To-do list

## Bugs to fix

## Future improvements

## Steps
1. Create super user
```
python manage.py createsuperuser
```