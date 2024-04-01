# rlctf_arena - Dynamic environment generation for training RL agents
This is a deliberately vulnerable web application with limited security measures taken. Do not run in a production environment

Its purpose is to act as a real world vulnerable application that generates vulnerable SQL queries for training reinforcement learning agents.
This code is only the backend environment, not the OpenAI Gym middleware.

To initialise: 
1. Configure environment choices in env.yml file
2. Initialise environment using env_logic.py script

# After initialise:
The database needs the foreign_key_check to be disabled for randomly generating a new vulnerable SQL query.
Connect to the MySQL DB database using the following:

To access the MySQL database manager:
http://(localhost)|(ipaddress):8080

MySQL DB Manager credentials:
Server - mysqldb
Username - root
password - password 

Once connected: 
1. Click on the classic models database
2. Select the SQL command window on the left of the UI
3. Enter "SET GLOBAL FOREIGN_KEY_CHECKS=0;" into the command UI
4. Select execute

# Other application info
To connect access the index.php:
http://(localhost)|(ipaddress):8000

To request new episode:
http://(localhost)|(ipaddress):8000/new_episode.php

Proposed topology: WAF not implemented

![alt text](https://github.com/chetwynrx/DynamicCTF/blob/main/env_topology_diagram.png)

# Limitations:
Currently a proof of concept
2. Disables foreign key assertions so that flags can be randomly inserted into the chosen database
2. Single client only - Each agent requires session management or a new environment when requesting new episode
3. HTML pages are not dynamic. Only the content for interfacing with the SQL backend is. The agent will always interact with the same HTML form input regardless of challenge type
4. Primarily focused only on SQL challenges. Will look into the development of XSS and other web application themed CTF challenges - A couple of test XSS sites are available

