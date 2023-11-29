release: python manage.py migrate
web: gunicorn server.wsgi
worker: celery -A server worker -l info
