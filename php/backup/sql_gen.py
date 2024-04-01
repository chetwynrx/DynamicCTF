

#   This SQL generator script is for Docker Host -> Docker Container. 
#   It is not the SQL generator script that runs on the PHP-Apache container

#   https://github.com/kayak/pypika - reference for generating the SQL query

from sqlite3 import Cursor
import time
start_time = time.time()



from pypika import Query, Table, Field, Criterion, Order, MySQLQuery
import yaml
import random
import string 
import MySQLdb
import fileinput
import sys
import requests as req 

tables = []
columns = []
varchar_cols = []
flag_insert_query = []
flag_index = []

db = MySQLdb.connect(
    host = 'mysqldb', 
    user = 'root', 
    passwd = 'password', 
    port = 3306)

def gen_Flag():

    flag_random = ''.join(random.choices(string.ascii_letters + string.digits, k = 4))
    flag = "{}{}{}".format("RL{",flag_random,"}")
    return flag




#db = MySQLdb.connect(
#    host = 'mysqldb', 
#    user = 'root', 
#    passwd = 'password', 
#    port = 3306)

#def gen_UpdateChallenge():  #   This is used to update the challenge
#    url = 'http://127.0.0.1:8000/new_episode.php'
#    resp = req.get(url)

    
#def get_amount_colsToUse():
#    env_file = open("env.yml", "r")
#    data = yaml.safe_load(env_file)

#    database_config = data[1]

#    max_columns_to_use = database_config["database"]["max_columns"]

#    columns = int(max_columns_to_use)

#    return columns


string_columns = ["hello", "world", "test", "string"]
int_columns = [1,2,3,4,5]
print(int_columns)

### Get Table Names
cursor = db.cursor()     # get the cursor
cursor.execute("USE classicmodels") # select the database
cursor.execute("SET foreign_key_checks = 0")
cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)

for (table_name,) in cursor:
    tables.append(table_name)

print(tables)

choose_random_table = random.choice(tables)

def gen_BoolQuery():
    
    count = 0
    
    ### Get Column Names
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database

    column_query = "SHOW COLUMNS FROM classicmodels.{};".format(choose_random_table)
    print("Columns are:", column_query)
    cursor.execute(column_query)    # execute 'SHOW TABLES' (but data is not returned)

    for (column_name) in cursor:
        columns.append(column_name[0])

    print(columns)

        ##### Create a list of varchar columns for SQL injection
    for element in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            print("True")
            varchar_cols.append(element)
    print("var columns: ", varchar_cols)

    ### Generate Random Select Query
    random_criterion = random.choice(varchar_cols)       # Select a random criterion


    RANDOM_SELECT_MULTIPLE = MySQLQuery.from_(choose_random_table).select(*random.sample(columns,3)) ### Make sure you use unpacking

    print("THIS IS THE QUERY: ", RANDOM_SELECT_MULTIPLE)

    WHERE = "WHERE {} = $data".format(random_criterion)



    random_query = "{} {}".format(RANDOM_SELECT_MULTIPLE, WHERE)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    #random_query = random_query.replace(", WHERE", " WHERE ")
    random_query = random_query.replace("$data", "'$data'" )
    print("The final query is:", random_query)


    f = open("query.txt", "w+")
    f.write(random_query +"\n")
    f.close()

    ### Get Datatype
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database
    cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, random_criterion)) # select the database

    value = cursor.fetchall()


    ### Modify Form Input Type to Match Database
    if "varchar" in str(value):
        form_input_type = "text"
    elif "int" in str(value):
        form_input_type="number"
    elif "decimal" in str(value):
        form_input_type="number"
    elif "smallint" in str(value):
        form_input_type="number"
    elif "text" in str(value):
        form_input_type="text"
    elif "date" in str(value):
        form_input_type="2022-09-01"
    elif "mediumtext" in str(value):
        form_input_type="text"

    print(form_input_type)
    

    #text = "#dynamic_form"   # if any line contains this text, I want to modify the whole line.
    #new_text = "{}{}{}{}{}{}".format("echo 'email: <input type=", '" ', form_input_type, ' " ', 'name="email" >', "' ; #dynamic_form")
    '''
    x = fileinput.input(files="php/src/index_3.php", inplace=1)

    for line in x:
        if text in line:
            line = new_text
        print(line),
    x.close()
    '''


    ### Insert Flag
    ### Write query into file

    flag = gen_Flag()

    cursor = db.cursor()

    #### Here we get all the database columns and set some default values based on the data type
    #### We need these default values so we can insert a new row into the database
    for column in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, column)) # select the database
        value = cursor.fetchall()
        if "varchar" in str(value):
            input = ""
        elif "int" in str(value):
            input = random.randint(0,150)
        elif "decimal" in str(value):
            input = random.randint(1, 150)
        elif "smallint" in str(value):
            input = random.randint(1,150)
        elif "text" in str(value):
            input = ""
        elif "date" in str(value):
            input = "2022-01-01"
        elif "mediumtext" in str(value):
            input = ""
        elif "mediumblob" in str(value):
            input = ""
        flag_insert_query.append(input)

    #### Check if the flag_insert_query is a string so we can modify the string default value
    for _ in flag_insert_query:
        if (type(_) is str):
            if "2022-01-01" in _:
                continue
            else:
                index = flag_insert_query.index(_)  # Append the list_index with the index value of all strings
                flag_index.append(index)

    #### Choose a random "Hello Hacker" and replace it with the flag string
    flag_insert_query[random.choice(flag_index)] = flag

    customers = str(Table(choose_random_table))
    customers = customers.replace('"',"")

    INSERT_TEST = MySQLQuery.into(customers).replace(*flag_insert_query)

    flag_archive = str(INSERT_TEST)

    print("This is the insert: ", INSERT_TEST)

    cursor = db.cursor()


    cursor.execute("{}".format(INSERT_TEST))

    db.commit()

    with open("flag.txt", "w") as my_file:
        my_file.write(flag_archive+"\n")


    #index = (flag_insert_query[flag_input])

    #print("Index: ", index)

    #while type(flag_input) == "str":
    #    print("String")
    
           #flag_insert_query[index] = flag
            #print(flag_insert_query)
            
           



    #while count <=len(columns):
    #    print("True")

    #### Get value type
    


    #gen_UpdateChallenge()



#print("--- %s seconds ---" % (time.time() - start_time))    #   For updating the query



def gen_UnionQuery():
    
    count = 0
    
    ### Get Column Names
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database

    column_query = "SHOW COLUMNS FROM classicmodels.{};".format(choose_random_table)
    print("Columns are:", column_query)
    cursor.execute(column_query)    # execute 'SHOW TABLES' (but data is not returned)

    for (column_name) in cursor:
        columns.append(column_name[0])

    print(columns)

        ##### Create a list of varchar columns for SQL injection
    for element in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            print("True")
            varchar_cols.append(element)
    print("var columns: ", varchar_cols)

    ### Generate Random Select Query
    random_criterion = random.choice(varchar_cols)       # Select a random criterion


    RANDOM_SELECT_MULTIPLE = MySQLQuery.from_(choose_random_table).select(*random.sample(columns,3)) ### Make sure you use unpacking

    UNION_PREFIX = "UNION ALL"
    UNION_CONDITION = "UNION"

    print("THIS IS THE QUERY: ", RANDOM_SELECT_MULTIPLE)

    WHERE = "WHERE {} = $data".format(random_criterion)

    UNION_QUERY = {}


    random_query = "{} {} {} {}".format(RANDOM_SELECT_MULTIPLE, WHERE, UNION_PREFIX, RANDOM_SELECT_MULTIPLE)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    #random_query = random_query.replace(", WHERE", " WHERE ")
    random_query = random_query.replace("$data", "'$data'" )
    print("The final query is:", random_query)


    f = open("query.txt", "w+")
    f.write(random_query +"\n")
    f.close()

    ### Get Datatype
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database
    cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, random_criterion)) # select the database

    value = cursor.fetchall()


    ### Modify Form Input Type to Match Database
    if "varchar" in str(value):
        form_input_type = "text"
    elif "int" in str(value):
        form_input_type="number"
    elif "decimal" in str(value):
        form_input_type="number"
    elif "smallint" in str(value):
        form_input_type="number"
    elif "text" in str(value):
        form_input_type="text"
    elif "date" in str(value):
        form_input_type="2022-09-01"
    elif "mediumtext" in str(value):
        form_input_type="text"

    print(form_input_type)
    

    #text = "#dynamic_form"   # if any line contains this text, I want to modify the whole line.
    #new_text = "{}{}{}{}{}{}".format("echo 'email: <input type=", '" ', form_input_type, ' " ', 'name="email" >', "' ; #dynamic_form")
    '''
    x = fileinput.input(files="php/src/index_3.php", inplace=1)

    for line in x:
        if text in line:
            line = new_text
        print(line),
    x.close()
    '''


    ### Insert Flag
    ### Write query into file

    flag = gen_Flag()

    cursor = db.cursor()

    for column in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, column)) # select the database
        value = cursor.fetchall()
        if "varchar" in str(value):
            input = flag
        elif "int" in str(value):
            input = random.randint(0,150)
        elif "decimal" in str(value):
            input = random.randint(1, 150)
        elif "smallint" in str(value):
            input = random.randint(1,150)
        elif "text" in str(value):
            input = flag
        elif "date" in str(value):
            input = "2004-10-19"
        elif "mediumtext" in str(value):
            input = flag
        elif "mediumblob" in str(value):
            input = ""
        flag_insert_query.append(input)

    print(flag_insert_query)

    customers = str(Table(choose_random_table))
    customers = customers.replace('"',"")

    INSERT_TEST = MySQLQuery.into(customers).replace(*flag_insert_query)

    flag_archive = str(INSERT_TEST)

    print("This is the insert: ", INSERT_TEST)

    cursor = db.cursor()


    cursor.execute("{}".format(INSERT_TEST))

    db.commit()

    with open("flag.txt", "w") as my_file:
        my_file.write(flag_archive+"\n")


    #index = (flag_insert_query[flag_input])

    #print("Index: ", index)

    #while type(flag_input) == "str":
    #    print("String")
    
           #flag_insert_query[index] = flag
            #print(flag_insert_query)
            
           



    #while count <=len(columns):
    #    print("True")

    #### Get value type
    


    #gen_UpdateChallenge()



#print("--- %s seconds ---" % (time.time() - start_time))    #   For updating the query


# Generator logic
with open("challenge_type.txt", "r") as my_file:
    for line in my_file:
        if "bool" in line:
            try:
                gen_BoolQuery()
            except:
                # Set a sleep time to let system catch up
                time.sleep(1.5)
                continue
        elif "union" in line:
            try:
                gen_UnionQuery()
            except:
                time.sleep(1.5)
                continue
        else:
            print("No challenge type supplied")
#gen_BoolQuery()
#gen_UnionQuery()