#!/bin/bash
pip install mod-wsgi
mod_wsgi-express module-config > /etc/apache2/sites-available/django.conf
echo "WSGIScriptAlias / /code/django/project/wsgi.py
WSGIPythonPath /code/django
<Directory /code/django/project>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
Alias /static/ /code/django/project/static/
<Directory /code/django/project/static>
  Require all granted
</Directory>" >> /etc/apache2/sites-available/django.conf
a2dissite 000-default
a2ensite django
service apache2 start

