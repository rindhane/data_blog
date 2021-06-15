import json
from .utilities import self_setup_class
import re
import datetime

class Database(self_setup_class):
    def __init__(self,**kwargs):
        self.tables=list()
        self.middleware=None
        self.checksum=None
        self.middlewareContext=None
        self.EntryHandler=None
        self.select=None
        super().__init__(**kwargs)
    def check_middleware(self):
        if self.middleware is not None:
            return True
        else :
            raise Exception("Middleware doesn't exist")
    def create_table(self,name,**kwargs):
        if not self.isTable(name):
            var=Table(name=name,**kwargs)
            self.tables.append(var)
            self.save_to_file()
            if self.middleware.tableCreate(name):
                return var
            print('table created underlying table storage already exist')
            return var
        print(f"can't create a table named {name}, as it already exist")
        return False
    def make_table_present(self,):
        for table in self.tables:
            if not self.middleware.table_accessible(table.name):
                print(f'following table={table.name} is not present')
            else:
                self.make_tableEntries_present(table)            
    def make_tableEntries_present(self,table):
        for index in table.getIndexes():
            self.isEntryAccessible(self.get_entry(table=table,entryIndex=index))
        return True
    def create_EntryHandler(self,**kwargs):
        if self.check_middleware():
            self.EntryHandler=EntryHandler(middleware=self.middleware,**kwargs)
            return self.EntryHandler
        raise Exception("Middleware for Entry doesn't exist")
    def list_tables(self):
        return self.tables
    def save_to_file(self):
        context=dict(self.__dict__)
        context['middleware']=self.middleware.__class__.__name__
        context['EntryHandler']=self.EntryHandler.__class__.__name__
        jsonString=Table.serialize({'__DATABASE__': context })
        self.middleware.save_database(jsonString)
        return self
    def load_from_file(self):
        JsonContent=self.middleware.load_database()
        context=Table.from_json(JsonContent)['__DATABASE__']
        self.tables=context['tables']
        self.make_table_present()
        return self
    def isTable(self,name):
        for idx,table in enumerate(self.tables):
            if table.name==name:
                return self.tables[idx]
        return None        
    def select_table(self,tableName):
        self.select=self.isTable(tableName)
        if self.select is None: 
            print('Table was not found')
        return self.select
    def new_entry(self,table,**kwargs):
        tmpEntry=self.create_EntryHandler(table=table,**kwargs)
        tmpEntry.setEntrySetters()
        return tmpEntry
    def get_entry(self,table,entryIndex):
        return self.new_entry(table=table,index=entryIndex)
    def checkEntry(self,table,entryIndex):
        if table is not None:
            if entryIndex in table.getIndexes():
                return self.get_entry(self,table,entryIndex)
            return None
        return None
    def isEntryAccessible(self,entry):
        if self.middleware.entry_accessible(entry) is not None:
            return entry
        print(f'Entry: {entry.table.name}>>{entry.index} content is not accessible')
        return entry
    def add_entry(self,entry):
        table=self.isTable(entry.getTable())
        if table is not None:
            table.addEntry(entry)
            self.save_to_file()
            return True
        return False
    def find_entry(self,tableName,entryIndex):
        table=self.isTable(tableName)
        if table is None:
            print(f"{tableName} is not available in database")
            return None
        entry=self.checkEntry(table,entryIndex)
        if entry is not None:
            return self.isEntryAccessible(entry)   
        print("entry doesn't exist in database")
        return None
    def delete_entry(self,table,entry):
        table.deleteEntry(entry)
        self.save_to_file()
        return self
    
class Table(self_setup_class):
    def __init__(self,**kwargs):
        self.indexEnd=0
        self.entriesIndex=list()
        self.EntrySetters=dict()
        super().__init__(**kwargs)
    def getIndexEnd(self):
        return self.indexEnd
    def autoIncrementKey(self):
        self.indexEnd=self.indexEnd+1
        return self.indexEnd
    def addEntryIndex(self,index):
        self.entriesIndex.append(index)
    def addEntry(self,entry):
        entry.setIndex(self.autoIncrementKey())
        entry=self.set_EntrySetters(entry)
        #refactor required: check what to do if push was not sucessful
        if entry.push():
            self.addEntryIndex(entry.index)
        return entry
    def deleteEntry(self,entry):
        entry.deleteExistence()
        self.entriesIndex.remove(entry.getIndex())
        return True
    def getIndexes(self):
        return self.entriesIndex
    def self_serialize(self):
        return self.__class__.serialize(self)
    @classmethod
    def serialize(cls,table):
        encoder=tableJsonEncoder()
        return encoder.encode(table)
    @classmethod
    def from_json(cls,jsonString):
        decoder=tableJsonDecoder()
        return decoder.decode(jsonString)
    def set_schema(self,schema):
        #make sure schema is a dict
        if self.EntrySetters is not None:
            self.EntrySetters['SCHEMA']=schema
            return self
        self.EntrySetters=dict({"SCHEMA":schema})
        return self
    def get_schema(self):
        #schema is a dict object
        if self.EntrySetters is None:
            return None
        return self.EntrySetters.get("SCHEMA",None)
    def set_EntrySetters(self,entry):
        if getattr(self,'EntrySetters',None) is None\
         and not isinstance(getattr(self,'EntrySetters',None),dict):
            setattr(entry,'SCHEMA',None) #check should empty dict should be provided
            print(f"Unable to set the setter keys\
             {getattr(self,'EntrySetters',None)} is not dict object")
            return entry
        setter=self.EntrySetters
        #passing the key to the entry object
        for key in setter:
            setattr(entry,key,setter[key])
        return entry            

class EntryHandler(self_setup_class):
    def __init__(self,**kwargs):
        self.tableName=None
        self.content=None
        self.index=None
        self.middleware=None
        self.outputFormatter=None
        super().__init__(**kwargs)
    def setTable(self,tableName):
        self.tableName=tableName
        return self
    def getTable(self):
        return self.tableName
    def setIndex(self,index):
        self.index=index
        return True
    def getIndex(self):
        return self.index
    def setContent(self,content):
        self.content=content
        return self
    def getContent(self):
        return self.content
    def setEntrySetters(self):
        if getattr(self,'table',None) is not None:
            self.tableName=self.table.name
            self=self.table.set_EntrySetters(self)
            return self
        print('table is not set to the entry')
    def push(self,**kwargs):
        if self.checkSchema() is not None and self.content is not None :
            self.content=self.schemaEncoding()
        self.middleware.store_entry(self)
        return self
    def read(self):
        self.content=self.middleware.get_entry(self)
        if self.checkSchema() is not None:
            self.content=self.schemaDecoding()
            self.makeSchemaCompatible()
        return self.content
    def updater(self,new_items_value):
        #ensure new_items_value is a dict
        if not isinstance(new_items_value,dict):
            raise Exception(f'provided data {new_items_value} is not a dict object')
        #get old_items 
        old_content=self.read()
        for key in new_items_value:
            old_content[key]=new_items_value[key]
        return self
    def checkSchema(self):
        #check whether schema has been defined on entry
        if getattr(self,'SCHEMA',None) is not None and isinstance(self.SCHEMA,dict):
            return getattr(self,'SCHEMA', None)
        print('schema is not set or is not a dict object')
        return None
    def makeSchemaCompatible(self):
        #enforcing schema 
        if not isinstance(self.content,dict) :
            print(f'content: {self.content} is not a dict type to enforce schema')
            return None
        #checking for unwanted fields
        for key in self.content:
            if key not in self.SCHEMA:
                print(f"following field:{key} is not in table:{self.tableName} schema")
                return None
        #settings None for fields whose were values not provided
        for key in self.SCHEMA:
            if key not in self.content:
                self.content[key]=None
        return True
    def schemaDecoding(self):
        return content_decoder(self.content)
    def schemaEncoding(self):
        if self.makeSchemaCompatible():
            return content_encoder(self.content,self)
        raise Exception(f'content is not compatible to schema:{self.SCHEMA}')
    def deleteExistence(self):
        return self.middleware.delete_entry(self)

def remove_AUTO(string):
    #it is assumed the string as auto in it
    pattern=re.compile("\$AUTO\$")
    result=pattern.match(string) #only matched from the start of the string
    if result:
        return result.string[result.span()[1]:]
    return string

def clean_schema(schema):
    pass #cleaning method is yet to be implemented as current scope is not clear about cleaning
    return schema

def content_encoder(obj,entry):
    schema=getattr(entry,'SCHEMA')
    for key in schema:
        if '$AUTO$'==schema[key]:
            obj[key]=entry.getIndex()
        if '$AUTO_DATETIME$'==schema[key]:
            obj[key]=datetime.datetime.now()
    return tableJsonEncoder().encode(obj)

def content_decoder(string):
    #string is assumed to json compatible
    return tableJsonDecoder().decode(string)

def where_filter(item,where):
    #where is none or a dict
    if where is not None:
        for key in where:
            if item.get(key,None)==where[key]:
                continue
            return None
        return item
    return item

class tableJsonEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, Table):
             return dict({'__TABLE__': obj.__dict__})
         if isinstance(obj,datetime.datetime):
             return dict({'__DATETIME__': obj.timestamp()})
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

class tableJsonDecoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_hook = self.converter
        self.scan_once = json.scanner.make_scanner(self)
    @staticmethod
    def converter(obj):
        if '__TABLE__' in obj and len(obj)==1:
            return Table(**obj['__TABLE__'])
        if '__DATETIME__' in obj and len(obj)==1:
            return datetime.datetime.fromtimestamp(obj['__DATETIME__'])
        return obj

class outputFormatter(self_setup_class):
    '''helper class to transform the content output to required output format'''
    def __init__(self,**kwargs):
        self._data=kwargs
        super().__init__(**kwargs)
    def items(self,):
        return list(self._data.items())
    def keys(self,):
        return list(self._data.keys())
    def __getitem__(self,tag):
        if not isinstance(tag,str):
            raise ValueError (f"{tag} is not string , provide key in string format" )
        return getattr(self,tag,None)