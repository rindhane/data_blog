
#****************************************
'''Environment Variables from host '''
import os
environ= dict()
#secrete_key variables 
environ['SECRET_KEY']=os.environ.get("SECRET_KEY")
#Db variables 
#environ ["DB_USER"] = os.environ.get("DB_USER")
#environ ["DB_PASS"] = os.environ.get("DB_PASS")
#environ ["DB_NAME"] = os.environ.get("DB_NAME")
#environ ["CLOUD_SQL_CONNECTION_NAME"] = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
#environ ['DB_LOCALHOST']=os.environ.get('DB_LOCALHOST')
#environ ["MODE"] =os.environ.get('MODE') #"cloud" or 'local'
environ ["CLIENT_SECRET"] =os.environ.get('CLIENT_SECRET') #"cloud" or 'local'
#****************************************



#***************************************
'''Logging Utilities'''
import logging
logger=logging.getLogger()
#***************************************


#***************************************
#SCHEMA for DATABASE

SCHEMA = dict(
    {
        'tables':{
            'ARTICLES':{
                'name_in_db':'articles',
                'primaryKey':"id",
                'fields':['title','body','author','create_date','id']
                },
            'USERS':{
                'name_in_db':'users',
                'primaryKey':"username",
                'fields':['name','email','username','password','registered_date','id']
            }
        }
    }
)


checkKey='primaryKey'
#***************************************

