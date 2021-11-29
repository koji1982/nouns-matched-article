#!/bin/bash
# このファイルの実行前に.gitignoreに記載した環境ファイルを用意しておく
mkdir django
docker-compose run web django-admin.py startproject project ./django
printf "password: "
stty -echo
read password
echo "$password" | sudo -S chown -R $USER:$USER .
stty echo
#ここでsettings.pyのSECRET_KEYを環境ファイルにコピーし、
#他の環境変数をsettings.pyに渡すように書き変えたら、
#一度runserverでlocalhostが表示されるか確認してみる

docker-compose run web python3 manage.py startapp articles

#作成したappのパスをsettings.pyに追記する
#models.pyを記入する

docker-compose run web python3 manage.py makemigrations articles
docker-compose run web python3 manage.py migrate

docker-compose run web python3 manage.py createsuperuser
name:admin_secret
address:test@sample.com
password:admin_password


