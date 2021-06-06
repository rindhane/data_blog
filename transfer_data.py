from FileDatabase.manager import Database,outputFormatter
from FileDatabase.MiddlewareSetup import localFileMiddleware
from utilities import SCHEMA,checkKey

#**initating the connection with the final databasess
fileWare=localFileMiddleware(filepath='FileDatabase/database.json',dataPath='FileDatabase')
db=Database(middleware=fileWare,)
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
import sqlalchemy
import os 
db_old_path=os.environ.get('DB_LOCALHOST')
db_old=sqlalchemy.create_engine(db_old_path)
curr=db_old.connect().execution_options(autocommit=True)

#************************

#***for article table***************
tableName='articles'
expression=f"select * from {tableName}"
result=curr.execute(expression).fetchall()

table=db.isTable(tableName)

for resultant in result:
    contentDict=dict(resultant.items())
    tmpEntry=db.new_entry(table=table,content=contentDict)
    db.add_entry(tmpEntry)

db.save_to_file()

#************************

tableName='users'
expression=f"select * from {tableName}"
result=curr.execute(expression).fetchall()

table=db.isTable(tableName)

for resultant in result:
    contentDict=dict(resultant.items())
    tmpEntry=db.new_entry(table=table,content=contentDict)
    db.add_entry(tmpEntry)

db.save_to_file()
#*******************************