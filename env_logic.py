import yaml
import random
import requests
import os
import sys
import subprocess
import fileinput
import shutil
import time

start_time = time.time()

php_docker_config = "docker_phpconfig/Dockerfile"

bool_queries = "php\\src\\bool.txt"
union_queries = "php\\src\\union.txt"
index_page = "php\\src\\index.php"
query_main_file = "php\\src\query.txt"
new_request = "localhost:8000/new_episode.php"
comment = "#dynamic_query"
prefix_q = ' if ($result = $conn->query(" '
suffix_q = ' ")) { '

def booleanBased ():
    lines = open(bool_queries).read().splitlines()
    query = random.choice(lines)
    return query 


def unionBased ():
    lines = open(union_queries).read().splitlines()
    query = random.choice(lines)
    return query 

def launch ():
    print("Starting")
    #os.system('cmd /k docker-compose up')
    #subprocess.call ('docker network create -d bridge --subnet 10.0.0.0/24 sql_network', cwd=os.getcwd())
    subprocess.call ('docker-compose up', shell="True", cwd=os.getcwd())
    #os.sleep(10)
    #subprocess.call ('docker network connect sql_network mysqldb', cwd=os.getcwd())
    #subprocess.call ('docker network connect sql_network php-apache', cwd=os.getcwd())
    #subprocess.call ('docker network connect sql_network database_admin_panel', cwd=os.getcwd())
    #subprocess.call ('docker network connect sql_network postgresdb', cwd=os.getcwd())

def copy_queries (file):
        with open(file,'r') as queries_to_choose, open(query_main_file,'w+') as modify_main_query_file:
            for line in queries_to_choose:
                modify_main_query_file.write(line)


    
    
    #if requests.head(new_request).status_code == requests.codes.ok:
    #    print("Online")
    #insert_query = requests.get("localhost:8000/new_episode.php")
    


def read_config(): # logic for reading env.yaml file configurations

    index_count = 0
    env_file = open("env.yml", "r")
    data = yaml.safe_load(env_file)

    vulnerability_config = data[0]
    database_config = data[1]
    #HTML_config = data[2]
    security_config = data[2]

    agents = vulnerability_config["details"]["number_of_agents"]

    if "boolean" in vulnerability_config["details"]["vulnerability_type"]:
        type_file = bool_queries

        #query = booleanBased()

        #dynamic_query = query

        #for line in fileinput.input(index_page, inplace=True):
        # Whatever is written to stdout or with print replaces
        # the current line
        #    if comment in line:
        #        print(prefix_q + dynamic_query + suffix_q + comment)
        #    else:
        #        sys.stdout.write(line)

        # copy_queries(type_file)

        #print("The query is:", query)

        with open("php/src/challenge_type.txt", "w") as my_file:
            my_file.write("bool")

    elif "union" in vulnerability_config["details"]["vulnerability_type"]:
        #type_file = union_queries

        #query = unionBased()

        #dynamic_query = query

        #for line in fileinput.input(index_page, inplace=True):
        # Whatever is written to stdout or with print replaces
        # the current line
        #    if comment in line:
        #        print(prefix_q + dynamic_query + suffix_q + comment)
        #    else:
        #        sys.stdout.write(line)

        with open("php/src/challenge_type.txt", "w") as my_file:
            my_file.write("union")
        
    elif "error" in vulnerability_config["details"]["vulnerability_type"]:
        print("ERROR TRUE")
        file = open(php_docker_config, "a")
        file.write("\n" + "RUN sed -i 's/;html_errors = On/html_errors = On/g' /usr/local/etc/php/php.ini" + "\n")
        file.write("RUN sed -i 's/display_errors = Off/display_errors = On/g' /usr/local/etc/php/php.ini" + "\n")
        file.close()

    #while index_count <= agents:
    #        shutil.copyfile("php/src/index.php", "php/src/index_"+str(index_count)+".php")
    #        index_count +=1


        
    



        ##copy_queries(type_file)

        #print("The query is:", query)

read_config()
launch()