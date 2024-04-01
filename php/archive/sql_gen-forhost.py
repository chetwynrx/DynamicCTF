

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
import re

tables = []
columns = []
columns_y = []
varchar_cols = []
varchar_cols_y = []
flag_insert_query = []
flag_index = []
remove_row = []

columns_to_use = random.randint(2,4)

db = MySQLdb.connect(
    host = '10.0.0.3', 
    user = 'root', 
    passwd = 'password', 
    port = 9906)

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
cursor.execute("SET foreign_key_checks = 0") # Workaround for inserting flags into datasets with foreign key assignments
cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)

for (table_name,) in cursor:
    tables.append(table_name)

print(tables)

choose_random_table = random.choice(tables)


#### Select two random tables as union_x and union_y, will be used by the union query generator
if len(tables) > 1:
    random_tables = random.sample(tables, 2)
    union_x = random_tables[0]
    union_y = random_tables[1]
else:
    union_x = tables
    union_y = tables

print("Union Table x: ", union_x)       #### For debugging
print("Union Table y: ", union_y)       #### For debugging

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

    random_cols_to_use = random.randint(1,len(columns))

    print(columns)

        ##### Create a list of varchar columns for SQL injection
    for element in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            print("True")
            varchar_cols.append(element)
    print("var columns: ", varchar_cols)

    columns_chosen_file = open("columns.txt","w")
    HTML_FORM_STRING_LIST = []

    try:
        for cc in columns:
            HTML_FORM_STRING = "{}{}{}{}{}{}{}".format('echo " <br/> <b>',cc,'</b>" . ',"$row['",cc,"'] . ", '" " ; #field-to-replace')
            HTML_FORM_STRING_LIST.append(HTML_FORM_STRING)
    except Exception as e:
        print(e)
        
    HTML_FORM_STRING_LIST[0] = HTML_FORM_STRING_LIST[0] + "#form-to-replace"

    for ccc in HTML_FORM_STRING_LIST:
        columns_chosen_file.write(ccc + "\n")


    columns_chosen_file.close()

    ### Generate Random Select Query
    random_criterion = random.choice(varchar_cols)       # Select a random criterion


    RANDOM_SELECT_MULTIPLE = MySQLQuery.from_(choose_random_table).select(*random.sample(columns,random_cols_to_use)) ### Make sure you use unpacking

    print("THIS IS THE FIRST SELECT QUERY: ", RANDOM_SELECT_MULTIPLE)

    WHERE = "WHERE {} = $data".format(random_criterion)



    random_query = "{} {}".format(RANDOM_SELECT_MULTIPLE, WHERE)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    #random_query = random_query.replace(", WHERE", " WHERE ")
    random_query = random_query.replace("$data", "'$data'" )
    print("The FINAL UNION QUERY IS:", random_query)


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
        form_input_type="text"
    elif "mediumtext" in str(value):
        form_input_type="text"

    print(form_input_type)

    print("TEST")
    

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
        remove_row.append(column)
        flag_insert_query.append(input)

    #### Check if the flag_insert_query is a string so we can modify the string default value
    for _ in flag_insert_query:
        if (type(_) is str):
            if "2022-01-01" in _:
                _ = "2022-01-02"
            else:
                index = flag_insert_query.index(_)  # Append the list_index with the index value of all strings
                flag_index.append(index)

    #### Choose a random "Hello Hacker" and replace it with the flag string
    random_index = random.choice(flag_index)
    flag_insert_query[random_index] = flag

    remove_row_gen = 'DELETE FROM `{}` WHERE `{}` = {}{}{};'.format(choose_random_table, remove_row[random_index], '"', flag, '"')

    f = open("remove_row.txt", "w")
    f.write(remove_row_gen)
    f.close()

    customers = str(Table(choose_random_table))
    customers = customers.replace('"',"")

    INSERT_TEST = MySQLQuery.into(customers).replace(*flag_insert_query)

    flag_archive = str(INSERT_TEST)

    print("This is the insert: ", INSERT_TEST)

    


    #cursor.execute("{}".format(INSERT_TEST))

    #try:
    #    cursor.execute("{}".format(INSERT_TEST))
    #except Exception as e:
    #    print(e)

    
    f = open("flag.txt", "w")
    f.write(flag_archive+"\n")
    f.close()

    cursor = db.cursor()

    
    db.commit()


def gen_UnionQuery():

    
    count = 0
    
    ### Get Column Names
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database

    column_query = "SHOW COLUMNS FROM classicmodels.{};".format(union_x)
    print("Columns are:", union_x)
    cursor.execute(column_query)    # execute 'SHOW TABLES' (but data is not returned)

    for (column_name) in cursor:
        columns.append(column_name[0])

    print(columns)

    column_query_y = "SHOW COLUMNS FROM classicmodels.{};".format(union_y)
    cursor.execute(column_query_y)

    for (column_name) in cursor:
        columns_y.append(column_name[0])

        ##### Create a list of varchar columns for SQL injection
    for element in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            print("True")
            varchar_cols.append(element)
    print("var columns: ", varchar_cols)

    ### Generate Random Select Query
    random_criterion = random.choice(varchar_cols)       # Select a random criterion

    random_columns_minima = min(len(columns), len(columns_y))
    random_columns_amount = random.randint(1,random_columns_minima)


    RANDOM_SELECT_MULTIPLE = MySQLQuery.from_(union_x).select(*random.sample(columns, random_columns_amount)) ### Make sure you use unpacking
    RANDOM_SELECT_MULTIPLE_Y = MySQLQuery.from_(union_y).select(*random.sample(columns_y,random_columns_amount))
    UNION_PREFIX = "UNION ALL"
    UNION_CONDITION = "UNION"

    print("THIS IS THE QUERY: ", RANDOM_SELECT_MULTIPLE)

    WHERE = "WHERE {} = $data".format(random_criterion)

    UNION_QUERY = {}


    random_query = "{} {} {} {}".format(RANDOM_SELECT_MULTIPLE, WHERE, UNION_PREFIX, RANDOM_SELECT_MULTIPLE_Y)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    #random_query = random_query.replace(", WHERE", " WHERE ")
    random_query = random_query.replace("$data", "'$data'" )
    print("The FINAL UNION QUERY IS:", random_query)


    f = open("query.txt", "w+")
    f.write(random_query +"\n")
    f.close()
    

    ### Get Datatype
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database
    cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, random_criterion)) # select the database

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
        form_input_type="text"
    elif "mediumtext" in str(value):
        form_input_type="text"

    print(form_input_type)

    ### NEEDS FIXING
    #remove_row.append(column)

    

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
        print(column)
        ### MODIFY THIS TO A DIFFERENT TABLE
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, column)) # select the database
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
        remove_row.append(column)

    print("FLAG_INSERT", flag_insert_query)

    #### Check if the flag_insert_query is a string so we can modify the string default value
    for _ in flag_insert_query:
        if (type(_) is str):
            if "2022-01-01" in _:
                continue
            else:
                index = flag_insert_query.index(_)  # Append the list_index with the index value of all strings
                flag_index.append(index)

    random_index = random.choice(flag_index)
    flag_insert_query[random_index] = flag
    remove_row_gen = 'DELETE FROM `{}` WHERE `{}` = {}{}{};'.format(union_x, remove_row[random_index], '"', flag, '"')
    try:
        print(remove_row_gen)
    except:
        print("Error")

    f = open("remove_row.txt", "w")
    f.write(remove_row_gen)
    f.close()

    customers = str(Table(union_x))
    customers = customers.replace('"',"")

    INSERT_TEST = MySQLQuery.into(customers).replace(*flag_insert_query)


    flag_archive = str(INSERT_TEST)

    print("This is the insert: ", INSERT_TEST)

    cursor = db.cursor()


    cursor.execute("{}".format(INSERT_TEST))

    

    f = open("flag.txt", "w")
    f.write(flag_archive+"\n")
    f.close()

    db.commit()



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

def gen_UnionQuery2(): #### Columns in same database
    
    count = 0
    
    ### Get Column Names
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database

    column_query = "SHOW COLUMNS FROM classicmodels.{};".format(union_x)
    print("Table is: ", union_x)
    cursor.execute(column_query)    # execute 'SHOW TABLES' (but data is not returned)

    for (column_name) in cursor:
        columns.append(column_name[0])

    print("Columns are: ", columns)

    backup = columns

    for line in backup:
        print("Backup 1", line)
    print(len(backup))


        ##### Create a list of varchar columns for SQL injection
    for element in columns:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            print("True")
            varchar_cols.append(element)
    print("var columns: ", varchar_cols)

    ### Generate Random Select Query
    random_criterion = random.choice(varchar_cols)       # Select a random criterion

    columns_without = list(columns)
    columns_without.remove(random_criterion)

    for line in backup:
        print("Backup 2", line)
    print(len(backup))


    print("Columns Appended Once: ", columns_without)

    random_columns_amount = random.randint(1,len(columns_without))

    

    random_sample_x = random.sample(columns, random_columns_amount)

    random_sample_y = random.sample(columns, random_columns_amount)

    compiled_columns = list(set(random_sample_x + random_sample_y))

    columns_chosen_file = open("columns.txt","w")
    HTML_FORM_STRING_LIST = []

    for cc in compiled_columns:
        HTML_FORM_STRING = "{}{}{}{}{}{}{}".format('echo " <br/> <b>',cc,'</b>" . ',"$row['",cc,"'] . ", '" " ; #field-to-replace')
        HTML_FORM_STRING_LIST.append(HTML_FORM_STRING)
        
    HTML_FORM_STRING_LIST[0] = HTML_FORM_STRING_LIST[0] + "#form-to-replace"

    for ccc in HTML_FORM_STRING_LIST:
        columns_chosen_file.write(ccc + "\n")


    columns_chosen_file.close()


    print("COLS1: ", random_sample_x, "COLS2: ", random_sample_y)


    RANDOM_SELECT_MULTIPLE_X = MySQLQuery.from_(union_x).select(*random_sample_x) ### Make sure you use unpacking
    RANDOM_SELECT_MULTIPLE_Y = MySQLQuery.from_(union_x).select(*random_sample_y) ### Make sure you use unpacking


    UNION_PREFIX = "UNION ALL"
    UNION_CONDITION = "UNION"

    print("THIS IS THE QUERY FOR FIRST SELECT: ", RANDOM_SELECT_MULTIPLE_X)
    print("THIS IS THE QUERY FOR SECOND SELECT: ", RANDOM_SELECT_MULTIPLE_Y)

    WHERE = "WHERE {} = $data".format(random_criterion)

    UNION_QUERY = {}


    random_query = "{} {} {} {} {}".format(RANDOM_SELECT_MULTIPLE_X, WHERE, UNION_PREFIX, RANDOM_SELECT_MULTIPLE_X, WHERE)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    #random_query = random_query.replace(", WHERE", " WHERE ")
    random_query = random_query.replace("$data", "'$data'" )
    print("The FINAL UNION QUERY IS:", random_query)


    f = open("query.txt", "w+")
    f.write(random_query +"\n")
    f.close()
    

    ### Get Datatype
    cursor = db.cursor()     # get the cursor
    cursor.execute("USE classicmodels") # select the database
    cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, random_criterion)) # select the database

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
        form_input_type="text"
    elif "mediumtext" in str(value):
        form_input_type="text"

    print(form_input_type)

    ### NEEDS FIXING
    #remove_row.append(column)

    

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
        print(column)
        ### MODIFY THIS TO A DIFFERENT TABLE
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(union_x, column)) # select the database
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
        else:
            input = ""
        flag_insert_query.append(input)

       

        remove_row.append(column)
    
    flag_duplicate_replace = []

    for i in flag_insert_query:
        if i not in flag_duplicate_replace:
            flag_duplicate_replace.append(i)
        else:
            flag_duplicate_replace.append(None)


    print("FLAG_INSERT", flag_duplicate_replace)

    #### Check if the flag_insert_query is a string so we can modify the string default value
    for _ in flag_duplicate_replace:
        if (type(_) is str):
            if "2022-01-01" in _:
                continue
            else:
                index = flag_duplicate_replace.index(_)  # Append the list_index with the index value of all strings
                flag_index.append(index)

    random_index = random.choice(flag_index)
    flag_insert_query[random_index] = flag

    remove_row_index = flag_duplicate_replace.index(flag)



    remove_row_gen = 'DELETE FROM `{}` WHERE `{}` = {}{}{};'.format(union_x, remove_row[remove_row_index], '"', flag, '"')
    try:
        print(remove_row_gen)
    except:
        print("Error")

    f = open("remove_row.txt", "w")
    f.write(remove_row_gen)
    f.close()

    customers = str(Table(union_x))
    customers = customers.replace('"',"")

    INSERT_TEST = MySQLQuery.into(customers).replace(*flag_duplicate_replace)


    flag_archive = str(INSERT_TEST)

    print("This is the insert: ", INSERT_TEST)

    cursor = db.cursor()

    try:
        cursor.execute("{}".format(INSERT_TEST))
    except Exception as e:
        print(e)

    
    try:
        f = open("php/src/flag.txt", "w")
        f.write(flag_archive+"\n")
        f.close()
        print("worked")
    except Exception as e:
        print(e)
        print("failed")


    db.commit()
    

#print("--- %s seconds ---" % (time.time() - start_time))    #   For updating the query


# Generator logic
with open("C:\\Users\\roberac_adm\\rlctf_arena\php\\src\\challenge_type.txt", "r") as my_file:
    for line in my_file:
        print("The challenge type is: ", line)
        if "bool" in line:
            try:
                gen_BoolQuery()
            except:
                # Set a sleep time to let system catch up
                #time.sleep(5)
                continue
        elif "union" in line:
            try:
                gen_UnionQuery2()
            except:
                #time.sleep(5)
                continue
        else:
            print("No challenge type supplied")
#gen_BoolQuery()
#gen_UnionQuery()
db.commit()