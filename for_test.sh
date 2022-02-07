#!/bin/bash
apt update
apt install -y curl unzip
conda install -y selenium
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y  --fix-broken ./google-chrome-stable_current_amd64.deb
rm google-chrome-stable_current_amd64.deb
CHROME_VERSION=$(google-chrome --version | sed 's/ //g' | sed 's/GoogleChrome//g')
curl -O https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
rm chromedriver_linux64.zip
