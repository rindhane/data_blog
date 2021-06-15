from .utilities import self_setup_class
import os
from .gcloudBucketHandler import (
    get_OauthCreds_from_serviceAccount,
    create_client,
    get_bucket,
    exceptions as gExceptions,
    get_a_blob,
    blobDownload_as_bytes,
    upload_content_blob,
    blobDelete,
    blobExists,
    create_bucket_class_location
    )
import json

#skeleton class for inheritance 
class Middleware(self_setup_class):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def save_database(self,string):
        pass
    def load_database(self):
        string=''#returns jsonString of Database
        return string
    def store_entry(self,entry):
        pass
    def delete_entry(self,entry):
        pass
    def get_entry(self,entry):
        pass
    def entry_accessible(self,entry):
        pass
    def checkTable(self,name):
        pass
    def tableCreate(self,name):
        pass
    def table_accessible(self,name):
        pass

#Middleware for local filesystem
class localFileMiddleware(Middleware):
    def __init__(self,**kwargs):
        self.filepath=None#'database.json'
        self.dataPath=None
        super().__init__(**kwargs)
    def load_database(self):
        with open(self.filepath,'r') as fp:
            string=fp.read()
        return string
    def save_database(self,string):
        with open(self.filepath,'w') as fp:
            fp.write(string)
        return True
    def getHeaders(self, entry):
        table=entry.getTable()
        index=entry.getIndex()
        if table is not None and index is not None :
            #here folders are tables
            path=('' if not self.dataPath else self.dataPath+'/')+\
                str(table)+'/'+str(index)+".dbEntry"
            return path
        else:
            raise Exception("entry is not completely valid for submission")
    def store_entry(self,entry):
        path=self.getHeaders(entry)
        with open(path,'w') as fp:
            fp.write(str(entry.content))
        return True
    def delete_entry(self,entry):
        path=self.getHeaders(entry)
        os.remove(path)
        return True
    def get_entry(self,entry):
        path=self.getHeaders(entry)  
        with open(path,'r') as fp:
            content=fp.read()
        return content
    def entry_accessible(self,entry):
        path =self.getHeaders(entry)
        if os.path.isfile(path):
            return True
        return None
    def get_table_path(self,tableName):
        path=('' if not self.dataPath else self.dataPath+'/')+str(tableName)
        return path
    def checkTable(self,name):
        return os.path.isdir(self.get_table_path(name))
    def tableCreate(self,name):
        if self.checkTable(name):
            return False
        os.mkdir(self.get_table_path(name))
        return True
    def table_accessible(self,name):
        if self.checkTable(name):
            return True
        print(self.get_table_path(name))
        os.mkdir(self.get_table_path(name))
        return True


class gcloudMiddleware(Middleware):
    def __init__(self,**kwargs):
        self.filepath=None #json_file_name for storing the complete db state
        self.datapath=None #it is bucket name designated for the database
        self.tablePath='$$__TABLEFILE__$$' #default file to save all the tables name
        self.service_account_path=None
        super().__init__(**kwargs)
        tmp=get_OauthCreds_from_serviceAccount(json_file_path=self.service_account_path)
        self.client=create_client(tmp)
        self.table_file_init()
    def table_file_init(self):
        bucket=self.get_connector()
        blob=get_a_blob(bucket,self.tablePath)
        if not blobExists(blob):
            #only create if the __tablefile___ doesn't exist
            #creating TABLEFILE
            #initiating blank __TABLEFILE___
            upload_content_blob(blob,json.dumps(list()))
        return blob
    def get_connector(self):
        if not isinstance(self.datapath, str):
            raise Exception(f'{self.datapath} is not consistent to connect to cloud storage')
        return get_bucket(self.client,self.datapath)
    def db_file(self):
        if not isinstance(self.filepath,str) :
            return None
        bucket=self.get_connector()
        blob=get_a_blob(bucket,self.filepath)
        return blob
    def load_database(self):
        db=self.db_file()
        if db is None:
            print('check filepath parameter, does not look consistent')
            return None
        return blobDownload_as_bytes(db).decode()
    def save_database(self,string):
        db=self.db_file()
        if db is None:
            print("check filepath parameter, can't connect to database")
            return None
        upload_content_blob(db,string)
        return True
    def get_tables_file(self):
        tablesBlob=get_a_blob(self.get_connector(),self.tablePath)
        return json.loads(
                blobDownload_as_bytes(tablesBlob).decode()
                )
    def checkTable(self,name):
        return name in self.get_tables_file()
    def save_tables_file(self,tablesList):
        tablesBlob=get_a_blob(self.get_connector(),self.tablePath)
        upload_content_blob(tablesBlob,json.dumps(tablesList))
        return True
    def tableCreate(self,name):
        if self.checkTable(name):
            return False
        tmpTable=self.get_tables_file()
        tmpTable.append(name)
        self.save_tables_file(tmpTable)
        return True
    def table_accessible(self,name):
        if self.checkTable(name):
            return True
        return self.tableCreate(name)
    def table_delete(self,name):
        tmpTables=get_tables_file()
        if name in tmpTables:
            tmpTables.remove(name)
            return True
        print(f'{name} is not in the tablesList')
        return False
    def getHeaders(self,entry):
        if not '/' in str(entry.getTable())+str(entry.getIndex()):
            path = str(entry.getTable())+'/'+str(entry.getIndex())
            if not path == self.tablePath and not path == self.filepath:
                if self.table_accessible(str(entry.getTable())):                
                    return path 
        raise Exception(
            f"entry's Table: {entry.getTable()} or {entry.getIndex()} not accessible"
            )
    def store_entry(self,entry):
        bucket=self.get_connector()
        if bucket is not None: 
            blob=get_a_blob(bucket,self.getHeaders(entry))
            upload_content_blob(blob,str(entry.content))
            return True 
        raise Exception(f"db: {self.datapath} not available")
    def get_entry(self,entry):
        bucket=self.get_connector()
        if bucket is not None: 
            blob=get_a_blob(bucket,self.getHeaders(entry))
            return blobDownload_as_bytes(blob).decode()
        raise Exception(f"db: {self.datapath} not available")
    def delete_entry(self,entry):
        bucket=self.get_connector()
        if bucket is not None: 
            blob=get_a_blob(bucket,self.getHeaders(entry))
            blobDelete(blob)
            return True
        raise Exception(f"db: {self.datapath} not available")
    def entry_accessible(self,entry):
        bucket=self.get_connector()
        if bucket is not None: 
            blob=get_a_blob(bucket,self.getHeaders(entry))
            if blobExists(blob):
                return True
            return None
        raise Exception(f"db: {self.datapath} not available")

    