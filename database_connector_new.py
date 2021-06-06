from FileDatabase.manager import  Database, outputFormatter, where_filter
from FileDatabase.MiddlewareSetup import localFileMiddleware
from utilities import SCHEMA,checkKey


#***initiating  the database*****
fileWare=localFileMiddleware(filepath='FileDatabase/database.json',dataPath='FileDatabase')
db=Database(middleware=fileWare,)
db.load_from_file()
#********************************


#***scripts for creating a fresh database ********
"""
table=db.create_table(name='articles')
SCHEMA_articles={'id':'$AUTO$','title':None, 'body':None, 'author':None , 'create_date':'$AUTO_DATETIME$'}
table.set_schema(SCHEMA_articles)
table=db.create_table(name='users')
SCHEMA_users={'id':'$AUTO$','name':None,'email':None,'username':'primaryKey','password':None , 'registered_date':'$AUTO_DATETIME$'}
table.set_schema(SCHEMA_users)
db.save_to_file()
"""
#********************************************************


def get_items(db=db, SCHEMA=SCHEMA, table=None, where=None):
    table=SCHEMA['tables'].get(table,{}).get('name_in_db',None)
    table=db.isTable(table)
    if table is None:
        return list()
    indexes=table.getIndexes()
    result=list()
    for index in indexes:
        item=db.get_entry(table,index).read()
        if where is not None:
            item=where_filter(item,where)
            if item is not None:
                item=outputFormatter(**item)
                result.append(item)
            continue
        if item is not None:
            item=outputFormatter(**item)
            result.append(item) 
    return result

def insert_item(db= db, SCHEMA=SCHEMA, table=None, insert=None):
    table=SCHEMA['tables'].get(table,{}).get('name_in_db',None)
    table=db.isTable(table)
    if table is None or insert is None:
        return False
    entry=db.new_entry(table,content=insert)
    db.add_entry(entry)
    return True

def update_item(db=db,SCHEMA=SCHEMA,table=None,set_items=None,where=None):
    table=SCHEMA['tables'].get(table,{}).get('name_in_db',None)
    table=db.isTable(table)
    if table is None or where is None or set_items is None:
        return False
    indexes=table.getIndexes()
    for index in indexes:
        entry=db.get_entry(table,index)
        content=entry.read()
        content=where_filter(content,where)
        if content is not None:
            entry.updater(set_items).push()
            return True
    return False

def delete_item(db=db,SCHEMA=SCHEMA,table=None,where=None):
    table=SCHEMA['tables'].get(table,{}).get('name_in_db',None)
    table=db.isTable(table)
    if table is None or where is None:
        return False
    indexes=table.getIndexes()
    for index in indexes:
        entry=db.get_entry(table,index)
        content=entry.read()
        content=where_filter(content,where)
        if content is not None:
            db.delete_entry(table,entry)
            return True
    return False

