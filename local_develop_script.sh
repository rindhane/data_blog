#! /usr/bin/env bash

#replace the below <temporary place holder> with the exact values 
#replace export with set and filename ending with .bat instead of .sh to work it on windows  
export CLOUD_SQL_CONNECTION_NAME='<gcloud projectname>:<database location>:<instance name>'
export DB_USER='<username>'
export DB_PASS='<password>'
export DB_NAME='<database name within the instance>'
export SECRET_KEY='<secret key>'
#if the cloud connection is to be made to the cloud instance make the mode to the cloud 
#export MODE="cloud" 

#generally above values are only used if the local app is connected to the cloud database

#instruction for running cloud_sql_proxy before using below development settings
#1. run below command to run cloud _sql_proxy
#./cloud_sql_proxy.binary -instances=<gcloud projectname>:<database location>:<instance name>=tcp:3306
#the port 3306 is arbitary can be chosed any other as required.
#get help at https://cloud.google.com/sql/docs/mysql/quickstart-proxy-test

#below local setting are used for local development is used and using the proxy auth binary named as cloud_sql_proxy.binary

export DB_LOCALHOST='mysql+pymysql://<username>:<password>@<localhost:port>/<database name>'
export MODE='local'

echo 'environment variables are set'

# running flask app
#make sure the python virtual env is activated 
python main.py


#help https://stackoverflow.com/questions/307198/remove-quotes-from-named-environment-variables-in-windows-scripts 


