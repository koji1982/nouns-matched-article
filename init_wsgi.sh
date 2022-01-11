#!/bin/bash
pip install mod-wsgi
mod_wsgi-express module-config > /etc/apache2/sites-available/django.conf
echo "WSGIScriptAlias / /code/djangodir/project/wsgi.py
WSGIPythonPath /code/djangodir
<Directory /code/djangodir/project>
  <Files wsgi.py>
    Require all granted
  </Files>
</Directory>
Alias /static/ /code/djangodir/project/static/
<Directory /code/djangodir/project/static>
  Require all granted
</Directory>" >> /etc/apache2/sites-available/django.conf
a2dissite 000-default
a2ensite django
service apache2 start
