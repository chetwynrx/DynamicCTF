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

database_name = "classicmodels"

tables = []
columns = []
columns_y = []
varchar_cols = []
varchar_cols_y = []
flag_insert_query = []
flag_index = []
remove_row = []

db = MySQLdb.connect(
    host = 'mysqldb', 
    user = 'root', 
    passwd = 'password', 
    port = 3306)

# Generate a flag
def gen_Flag():

    flag_random = ''.join(random.choices(string.ascii_letters + string.digits, k = 4))
    flag = "{}{}{}".format("RL{",flag_random,"}")
    return flag

# Get table names for setting up the random queries
cursor = db.cursor()
cursor.execute("USE {}".format(database_name))
cursor.execute("SET GLOBAL foreign_key_checks = 0")
cursor.execute("SHOW TABLES")

for (table_name,) in cursor:
    tables.append(table_name)

print("Available Tables: {} \n".format(tables))

# Choose a random table for bool based challenge
choose_random_table = random.choice(tables)

# Select two random tables
if len(tables) > 1:
    random_tables = random.sample(tables, 2)
    union_x = random_tables[0]
    union_y = random_tables[1]
else:
    union_x = tables
    union_y = tables 

print("First table: {} Second Table: {} \n".format(union_x, union_y))

# commit the foreign key disable
#db.commit()

# Generate a bool query
def gen_BoolQuery():

    columns_chosen_file = open("columns.txt","w")
    HTML_FORM_STRING_LIST = []

    count = 0
    
    # Get column names
    try:
        cursor = db.cursor()
        cursor.execute("USE {}".format(database_name)) # select the database
        column_query = "SHOW COLUMNS FROM {}.{};".format(database_name, choose_random_table)

        cursor.execute(column_query)

        for (column_name) in cursor:
            columns.append(column_name[0])

    except Exception as e:
        print(e)

    print("Columns available: {}".format(columns))

    random_col_range = random.randint(1,len(columns))

    columns_to_use = random.sample(columns, random_col_range)
    print("Columns to use: {}".format(columns_to_use))


    # Setup the preprocessed webform for the HTML based on the columns
    try:
        for columnName in columns_to_use:
            HTML_FORM_STRING = "{}{}{}{}{}{}{}".format('echo " <br/> <b>',columnName,'</b>" . ',"$row['",columnName,"'] . ", '" " ; #field-to-replace')
            HTML_FORM_STRING_LIST.append(HTML_FORM_STRING)
    except Exception as e:
        print(e)
    HTML_FORM_STRING_LIST[0] = HTML_FORM_STRING_LIST[0] + "#form-to-replace"

    try:
        for formName in HTML_FORM_STRING_LIST:
            columns_chosen_file.write(formName + "\n")
    except Exception as e:
        print(e)

    columns_chosen_file.close()

    # Identify the varchar field types
    for element in columns_to_use:
        cursor.execute("SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{}' AND COLUMN_NAME = '{}';".format(choose_random_table, element)) # select the database
        datatype = cursor.fetchall()
        if "varchar" in str(datatype):
            varchar_cols.append(element)
    
    print("var columns: ", varchar_cols)

    # Generate random select criterion
    try:
        if len(varchar_cols) >=1:
            random_criterion = random.choice(varchar_cols)
            print("Random Criterion is: {}".format(random_criterion))
    except:
        print("Failed - No available varchar in chosen table. Re run or reconfigure database")
        

    # Format the select query
    BOOL_SELECT = MySQLQuery.from_(choose_random_table).select(*columns_to_use)

    # Format the operator to match the PHP
    WHERE = "WHERE {} = $data".format(random_criterion)

    # Generate the random query and strip any string characters
    # Also run some preprocessing
    random_query = "{} {}".format(BOOL_SELECT, WHERE)
    random_query = str(random_query)
    random_query = random_query.lstrip('(').rstrip(')')
    random_query = random_query.replace("'", '')
    random_query = random_query.replace('"', '')
    random_query = random_query.replace(",", ', ')
    random_query = random_query.replace("$data", "'$data'" )

    print("The FINAL UNION QUERY IS:", random_query)

    # Output final query to query file for archiving
    f = open("query.txt", "a")
    f.write(random_query + "\n")
    f.close()

    # generate the flag
    flag = gen_Flag()

    # Insert flag
    try:
        cursor.execute("SELECT {} FROM {} ORDER BY RAND() limit 1 ;".format(random_criterion, choose_random_table))
        new_flag_insert = cursor.fetchall()
        new_flag_insert = str(new_flag_insert)
        new_flag_insert = str(new_flag_insert.replace("(","").replace(")","").replace(",","")).replace("'","")

        cursor.execute('UPDATE {} SET {} = "{}" WHERE {} = "{}" LIMIT 1;'.format(choose_random_table, random_criterion, flag, random_criterion, new_flag_insert))

    except Exception as e:
        print(e)

    # Create the removal flag
    remove_row_gen_new = 'DELETE FROM {} WHERE {} = "{}" LIMIT 1;'.format(choose_random_table, random_criterion, flag)

    db.commit()

    try:
        f = open("flag.txt", "a")
        #f.write(flag_archive+"\n")
        f.write(remove_row_gen_new+"\n")
        #f.write(flag+"\n")
        f.close()
        print("worked")
    except Exception as e:
        print(e)
        print("failed")

    try:
        f = open("remove_row.txt", "w")
        #f.write(flag_archive+"\n")
        f.write(remove_row_gen_new+"\n")
        #f.write(flag+"\n")
        f.close()
        print("worked")
    except Exception as e:
        print(e)
        print("failed")

    db.commit()



    #try:
    #    for columnName in HTML_FORM_STRING_LIST:
    #        print("Adding {} to file".format(columnName))
    #        columns_chosen_file.write(columnName + "\n")
    #except Exception as E:
    #    print(E)



gen_BoolQuery()