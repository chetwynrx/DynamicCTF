# BASIC TESTING OF QUERY REGEN API

import requests
import random
from time import sleep


_ = 0

payload_file = "../payloads/union.txt"

#lines = open(payload_file).read().splitlines()
#myline =random.choice(lines)
#print(myline)

loop = 0
while loop <= 10:
    _ = 0
    print("Iteration:", loop)
    try:
        while _ <= 1000:
            print(_)
            #lines = open(payload_file).read().splitlines()
            #payload =random.choice(lines)

            #payload = {"email":payload}
            #p = requests.post('http://127.0.0.1:8000/', data=payload)
            p = requests.post('http://127.0.0.1:8000/new_episode.php')

            _+=1
            #print(_, payload)
    except Exception as E:
        print(E)
        print("Sleeping for 5 seconds due to max retries")
        sleep(5)

        #try:
        #    reset = requests.get('http://127.0.0.1:8000/new_episode.php')
        #    sleep(5)
        #except Exception as E:
        #    print(E)
        #    input()

    print("Resetting")
    
    loop +=1
