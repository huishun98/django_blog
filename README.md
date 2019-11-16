# Django Blog

## Description
This is a blog built using Django with a PostgreSQL database. The live example can be found here: https://hs-django-blog.herokuapp.com/.

You may log in with these credentials:
- username: admin
- password: password

This blog is meant for bloggers who want a fully customisable blog/website with a fully customisable content management system.

The design of this blog is meant to be minimalistic and easily changed and customised to fit its user's vision.

## Features
On top of basic CRUD functionality, this web app has several other features:
1. Mobile first, mobile and web responsive
2. Downloading and uploading of blog content for backup purposes
3. Categorisation of posts

## Steps to deploy code (using Heroku and AWS S3)
1. Fork this repository.
2. Create a Heroku account and initialise a new application. Deploy the forked repository to Heroku.
3. Create and configure AWS S3 account to store media files

Create a new bucket and add the following code into Permissions > Bucket Policy
```
{
    "Version": "2012-10-17",
    "Id": "http referer policy example",
    "Statement": [
        {
            "Sid": "Allow get requests originating from www.example.com and example.com.",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<host-name>/*",
            "Condition": {
                "StringLike": {
                    "aws:Referer": [
                        "http://127.0.0.1:8000/*",
                        "<host-name>/*"
                    ]
                }
            }
        }
    ]
}
```
4. Create Heroku Postgres database under resources
5. Configure Heroku Config Vars at Heroku settings.

The configuration should include:

From AWS:
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- S3DIRECT_REGION

From Heroku:
- DATABASE_PASSWORD
- DATABASE_NAME
- DATABASE_USER
- DATABASE_HOST
- ENVIRONMENT_TYPE (production for production, debug for debug)

6. Change HOSTNAME and ALLOWED_HOSTS in settings.py file from hs-django-blog to the created Heroku application name
7. Deploy on Heroku
8. On Heroku console, make migrations.
```
python mange.py migrate
```
On the same console, create super user (admin)
```
python manage.py createsuperuser
```


## Steps to run locally
1. Set up virtual environment
```
virtualenv env
source env/bin/activate
```
2. Install packages
```
pip install -r requirements.txt --no-index
```
3. Set up local Postgres database and update settings in settings.py
```
createdb blog_code
python manage.py migrate
```

To set up postgres locally,
```
lunchy start postgres
psql postgres -U <username>
psql postgres (cntr-d to quit)
```

To add env variabes,
```
heroku config:get CONFIG-VAR-NAME -s  >> .env
```
See steps to deploy code (above) for the required environment variables.

4. Run code
```
python manage.py runservers
```
