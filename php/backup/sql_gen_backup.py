#!/usr/bin/env python3
#TEST2
#   https://github.com/kayak/pypika

from pypika import Query, Table, Field, Criterion, Order
import yaml
import random
import MySQLdb
import sys
import fileinput
import sys

tables = []
columns = []


db = MySQLdb.connect(
    host = 'mysqldb', 
    user = 'root', 
    passwd = 'password', 
    port = 3306)

    
def get_amount_colsToUse():
    env_file = open("env.yml", "r")
    data = yaml.safe_load(env_file)

    database_config = data[1]

    max_columns_to_use = database_config["database"]["max_columns"]

    columns = int(max_columns_to_use)

    return columns


string_columns = ["hello", "world", "test", "string"]
int_columns = [1,2,3,4,5]
print(int_columns)

### Example pypika query
accounts = Table('accounts')
q = Query.from_(accounts).select(
    accounts.revenue - accounts.cost
)

### Get Table Names
cursor = db.cursor()     # get the cursor
cursor.execute("USE classicmodels") # select the database
cursor.execute("SHOW TABLES")    # execute 'SHOW TABLES' (but data is not returned)

for (table_name,) in cursor:
    tables.append(table_name)

print(tables)

choose_random_table = random.choice(tables)

### Get Column Names
cursor = db.cursor()     # get the cursor
cursor.execute("USE classicmodels") # select the database

column_query = "SHOW COLUMNS FROM classicmodels.{};".format(choose_random_table)
print(column_query)
cursor.execute(column_query)    # execute 'SHOW TABLES' (but data is not returned)

for (column_name) in cursor:
    columns.append(column_name[0])

print(columns)

### Generate Random Select Query
random_criterion = random.choice(columns)       # Select a random criterion 

RANDOM_SELECT_MULTIPLE = Query.from_(choose_random_table).select(*random.sample(columns,3)) ### Make sure you use unpacking

WHERE = "WHERE {} = $data".format(random_criterion)

print(RANDOM_SELECT_MULTIPLE, WHERE)

random_query = "{}{}{}".format(RANDOM_SELECT_MULTIPLE, " ",WHERE)        # Combine the two together

########################################## Cleaning of query. Bit of a hack, could be better
random_query = str(random_query)
random_query = random_query.lstrip('(').rstrip(')')
random_query = random_query.replace("'", '')
random_query = random_query.replace('"', '')
random_query = random_query.replace(",", ', ')
random_query = random_query.replace(", WHERE", " WHERE ")
random_query = random_query.replace(",  WHERE", " WHERE ")
random_query = random_query.replace("$data", "'$data'" )
print(random_query)

### Write query into file

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
    form_input_type="date"
elif "mediumtext" in str(value):
    form_input_type="text"

print(form_input_type)

text = "#dynamic_form"   # if any line contains this text, I want to modify the whole line.
new_text = "{}{}{}{}{}{}".format("echo 'email: <input type=", '" ', form_input_type, ' " ', 'name="email" >', "' ; #dynamic_form")
x = fileinput.input(files="index.php", inplace=1)
for line in x:
    if text in line:
        line = new_text
    print(line),
x.close()
