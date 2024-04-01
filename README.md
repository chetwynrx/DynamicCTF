# rlctf_arena
Reinforcement Learning Training for CTF

To initialise: 
1. Configure environment choices in env.yml file
2. Initialise environment using env_logic.py script

To connect:
http://(localhost)|(ipaddress):8000

To request new episode:
http://(localhost)|(ipaddress)/new_episode.php

Proposed topology: WAF not implemented

![alt text](https://github.com/chetwynrx/DynamicCTF/blob/main/env_topology_diagram.png)

Limitations:
1. Inserting flag row data into the database will replace any duplicate row entries in the original database
2. Disables foreign key assertions so that flags can be randomly inserted into the chosen database
2. Single client only - Each agent requires session management or a new environment when requesting new episode - Will look into best solution
3. HTML pages are not dynamic so the agent will always interact with the same HTML form input regardless of challenge type
4. Currently focused only on SQL challenges. Will look into the development of XSS and other web application themed CTF challenges

