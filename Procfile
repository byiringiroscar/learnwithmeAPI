web: gunicorn learn_with_me.wsgi
release: python manage.py makemigrations --noinput
release : python manage.py collectstatic --noinput
release: python manage.py migrate --noinput
