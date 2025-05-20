web: gunicorn main_chat.wsgi --log-file - 
web: python manage.py migrate && gunicorn main_chat.wsgi