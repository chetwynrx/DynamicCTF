import requests
import random
from time import sleep
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


_ = 0

payload_file = "payloads/union.txt"

#lines = open(payload_file).read().splitlines()
#myline =random.choice(lines)
#print(myline)

def retry_session(retries=10):
    session = requests.Session()
    retries = Retry(total=retries,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504],
                method_whitelist=frozenset(['GET', 'POST']))

    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))

    return session

loop = 0
while loop <= 10:
    _ = 0
    print("Iteration:", loop)
    try:
        while _ <= 1000:
            lines = open(payload_file).read().splitlines()
            payload =random.choice(lines)

            payload = {"email":payload}

            session = retry_session(retries=10)
            session.post('http://127.0.0.1:8000/', data=payload, timeout=1)

            print(_, payload)

            _+=1
            #print(_, payload)
    except:
        continue

    try:
        reset = session.get('http://127.0.0.1:8000/new_episode.php')
        sleep(5)
    except Exception as E:
        print(E)
        continue

    print("Resetting")
    
    loop +=1
