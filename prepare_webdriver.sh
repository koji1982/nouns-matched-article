#!/bin/bash
apt-get update
apt-get install -y firefox
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar -zxvf geckodriver-v0.30.0-linux64.tar.gz
mv geckodriver /usr/local/bin/
