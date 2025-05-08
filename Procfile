web: gunicorn main_chat.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn main_chat.wsgi