from FileDatabase.manager import Database
from FileDatabase.MiddlewareSetup import gcloudMiddleware
from utilities import SCHEMA,checkKey

#**initating the connection with the final databasess
fileWare=gcloudMiddleware(filepath='database.json', 
                         datapath='database-cloud',
                         service_account_path='client_secret.json'
                         )
db=Database(middleware=fileWare)
db.load_from_file()
#*********************************************************


#***scripts for creating a fresh database ********
"""
table=db.create_table(name='articles')
SCHEMA_articles={'id':'$AUTO$','title':None, 'body':None, 'author':None,'create_date':'$AUTO_DATETIME$' }
table.set_schema(SCHEMA_articles)
table=db.create_table(name='users')
SCHEMA_users={'id':'$AUTO$','name':None,'email':None,'username':'primaryKey','password':None,'registered_date':'$AUTO_DATETIME$' }
table.set_schema(SCHEMA_users)
db.save_to_file()
"""
#********************************************************


#**************************
#connecting old database
from FileDatabase.manager import Database,outputFormatter
from FileDatabase.MiddlewareSetup import localFileMiddleware
from utilities import SCHEMA,checkKey
fileWare=localFileMiddleware(filepath='FileDatabase/database.json',
                                dataPath='FileDatabase')
db_old=Database(middleware=fileWare,)
curr=db_old.load_from_file()

#************************


#***************************
def table_entries_transfer(tableName,db_new,db_old):
    table_old=db_old.isTable(tableName)
    table_new=db_new.isTable(tableName)
    for index in table_old.getIndexes():
        contentDict=db_old.get_entry(table_old,index).read()
        tmpEntry=db_new.new_entry(table=table_new,content=contentDict)
        db_new.add_entry(tmpEntry)
        print(f'entry:{index} in table:{tableName} has been transferred')
    db.save_to_file()
    return True
#****************************

#***for article table***************
tableName='articles'
table_entries_transfer(tableName,db,curr)

#*****for users table*******************

tableName='users'
table_entries_transfer(tableName,db,curr)

#*******************************

print('Transfer done')