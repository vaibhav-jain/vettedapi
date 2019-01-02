# VettedAPI
POC for Vetted

## Setup Instructions ##
1. Make sure you have Django-2.0.9 installed on your system
2. Install requirements by running this command from your project dir

  On Prod:

  `pip install -r requirements.txt`

  On Dev:

  `pip install -r requirements/dev.txt`

3. Setup these environment variables on your system (or in virtualenv)

On Windows

```
  set "DEBUG=True"
  set "DJANGO_SETTINGS_MODULE=config.settings.dev"
  set "SECRET_KEY=xxxxxYourxxSecretxxKeyxxxxx"
  set "DATABASE_URL=psql://username:password@127.0.0.1:5432/dbname"
  set "EMAIL_HOST=smtp.something.com"
  set "EMAIL_HOST_USER=youremail@something.com"
  set "EMAIL_HOST_PASSWORD=yoursecretpassword"
```

  On Linux

```
  export DEBUG='TRUE'
  export DJANGO_SETTINGS_MODULE='config.settings.dev'
  export SECRET_KEY='xxxxxYourxxSecretxxKeyxxxxx'
  export DATABASE_URL='psql://username:password@127.0.0.1:5432/dbname'
  export "EMAIL_HOST=smtp.something.com"
  export "EMAIL_HOST_USER=youremail@something.com"
  export "EMAIL_HOST_PASSWORD=yoursecretpassword"
```

You can also save these in your virtualenv's script for auto invocation during virtualenv initialization

4. Apply Migrations by running this command from the project dir

  `python manage.py migrate`

5. Create Super User

  `python manage.py createsuperuser`

6. Finally run your dev server by running this command from your project dir

  `python manage.py runserver`

# Goodies Included #
1. Separate settings for development and production environment
2. Settings based on [django-environ](https://django-environ.readthedocs.org/en/latest/)
3. Excellent admin interface by [django-grappelli](https://django-grappelli.readthedocs.org/en/latest/index.html)
4. Static file serving with [whitenoise](https://github.com/evansd/whitenoise)
5. Extra commands by [django-extensions](https://github.com/django-extensions/django-extensions)

### Help ###
1. Use this to generate [SECRET_KEY](http://www.miniwebtool.com/django-secret-key-generator/)