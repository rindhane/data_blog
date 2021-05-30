from utilities import environ, SCHEMA, checkKey
import sqlalchemy


if environ["MODE"] =="cloud":
    db= sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=environ["DB_USER"],
            password=environ["DB_PASS"],
            database=environ["DB_NAME"],
            query={"unix_socket":"/cloudsql/{}".format(environ["CLOUD_SQL_CONNECTION_NAME"])},
        ),
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
        pool_recycle=1800,

    )
elif environ["MODE"] =="local" :
    db=sqlalchemy.create_engine(environ['DB_LOCALHOST'])
else :
    raise Exception("DataBase mode not defined in the environ")
    

#helper_function for wrapping string in one more layer of quotes
def quote_string(string):
    string="'"+string+"'"
    return string

#helper_function to add where clause
def add_where_clause(execute_string,where):
    tmp_tuple=tuple(where.items())[0]# here where is assumed to be dict with only one key pair
    field=tmp_tuple[0]
    value=tmp_tuple[1]
    execute_string=execute_string+f" WHERE {field} = {quote_string(str(value))} "
    return execute_string

def execute_action_db(db, execute_string, fetch=True):
    #create cursor and execute the action
    curr = db.connect().execution_options(autocommit=True)
    response = curr.execute(execute_string)
    # above execution gets auto-commited 
    #retrieving the result into new variable
    if fetch :
        result = response.fetchall()
        #closing the proxy object of sqlalchemy
        response.close()
        curr.close()
        return result
    #closing the proxy object of sqlalchemy
    response.close()
    curr.close()
    return True

#function to retrieve items from the given table
def get_items(db=db, SCHEMA=SCHEMA, table=None, where=None):
    if table == None : 
        return list()
    #get table from schema 
    table=SCHEMA['tables'][table]['name_in_db']
    SELECT_EXPRESSION=f"select * from {table}" #SQL expression to get all items
    execute_string=SELECT_EXPRESSION
    if where:
        execute_string=add_where_clause(execute_string,where)
    return execute_action_db(db,execute_string)

#helper function to convert fields in a list to a string
def convert_list_string(tmpList):
    result =''
    separator=','
    spaceGap= ' ' 
    checker=len(tmpList)
    for i, item in enumerate(tmpList):
        if i < checker -1:
            result = result+str(item)+separator+spaceGap
        else :
            result = result+str(item)+spaceGap
    return result


def convert_dict_to_fieldValueString(tmpDict):
    fields=list(tmpDict.keys())
    field_string=convert_list_string(fields)
    values=[quote_string(tmpDict[field]) for field in fields]
    values_string=convert_list_string(values)
    return field_string, values_string


def insert_item(db= db, SCHEMA=SCHEMA, table=None, insert=None):
    if table==None or insert==None:
        return False
    #get fields and table from insert(a dict object)
    fields, values = convert_dict_to_fieldValueString(insert)
    #build SQL insert EXPRESSION 
    INSERT_EXPRESSION=f"INSERT INTO\
    {SCHEMA['tables'][table]['name_in_db']}({fields})\
      VALUES({values})"
    return execute_action_db(db=db, execute_string=INSERT_EXPRESSION, fetch=False)


def create_set_string(set_items):
    string=""
    equalString = '='
    gap=' '
    separator=',' 
    end=len(set_items)-1
    for idx,field in enumerate(set_items): #set_items is considered a dict
        string= string + gap + str(field) +\
                               equalString +\
                               gap +\
                               quote_string(str(set_items[field])) +\
                               (separator if idx < end else gap)
    return string

def update_item(db=db,SCHEMA=SCHEMA,table=None,set_items=None,where=None):
    if table==None or where==None or set_items==None:
        return False
    set_string=create_set_string(set_items)
    UPDATE_EXPRESSION=f"UPDATE {SCHEMA['tables'][table]['name_in_db']} set {set_string} "
    UPDATE_EXPRESSION=add_where_clause(execute_string=UPDATE_EXPRESSION,
                                      where=where)
    return execute_action_db(db=db, execute_string=UPDATE_EXPRESSION, fetch=False)

def delete_item(db=db,SCHEMA=SCHEMA,table=None,where=None):
    if table==None or where==None :
        return False
    DELETE_EXPRESSION=f"DELETE FROM {SCHEMA['tables'][table]['name_in_db']} "
    DELETE_EXPRESSION=add_where_clause(execute_string=DELETE_EXPRESSION,
                                      where=where,
                                      )
    return execute_action_db(db=db, execute_string=DELETE_EXPRESSION, fetch=False)
    

