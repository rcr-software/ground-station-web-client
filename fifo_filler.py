
import time
import random
f = open('datastream', 'w', buffering=1) # line buffered file writing
while True:
    time.sleep(0.2)
    x = random.randint(1, 20)
    print(x)
    f.write(str(x) + '\n')
