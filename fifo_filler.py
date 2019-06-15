import json
import time
import random
x =  32.3946993
y = -106.4729961
dx = 0
dy = 0
z = 0
dz = 10


f = open('datastream', 'w', buffering=1) # line buffered file writing
while True:
    time.sleep(0.2)
    dx += 0.001 * (random.random() * 2 - 1)
    dy += 0.001 * (random.random() * 2 - 1)
    dx *= 0.9
    dy *= 0.9
    x += dx
    y += dy
    z += dz
    dz -= 0.5
    if z < 0:
        dz = 10

    data = json.dumps([x,y,z])
    print(data)
    f.write(data + '\n')
