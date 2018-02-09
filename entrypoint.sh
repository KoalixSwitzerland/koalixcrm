#!/bin/bash

# Install dependencies
pip install -r development_requirements.txt

# Install FOP 2.2
wget https://archive.apache.org/dist/xmlgraphics/fop/source/fop-2.2-src.tar.gz
tar -xzf fop-2.2-src.tar.gz -C ../usr/bin
rm -rf fop-2.2-src.tar.gz

# Install Java 8
wget --no-check-certificate -c --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u162-b12/0da788060d494f5095bf8624735fa2f1/jdk-8u162-linux-x64.tar.gz
tar -xzf jdk-8u162-linux-x64.tar.gz -C ../usr/bin
rm -rf jdk-8u162-linux-x64.tar.gz

# Execute startup scripts
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000