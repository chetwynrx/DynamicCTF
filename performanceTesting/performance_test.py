import os
import time

start_time = time.time()

for i in range(10000000):
    os.system("python sql_gen-forhost.py")

print("--- %s seconds ---" % (time.time() - start_time))