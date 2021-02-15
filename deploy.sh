#!/usr/bin/env bash

#make sure working directory or current directory is the root folde of project
rm -r static/*
rm -r about/static/* ;
rm -r about/templates/about/* ;
cd about/ ;
npm run build ; #make sure npm is installed
cd ../ ;
python manage.py collectstatic ; # make sure right pyenv is activated.
gcloud app deploy ;# make sure right project in Gcloud is selected 



