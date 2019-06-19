import math
import json
import time
import random

import mysql.connector

def connect_database(host):
    db = mysql.connector.connect(
            host=host,
            db="GCDB",
            user="root",
            passwd="qazwsx",
            #auth_plugin='caching_sha2_password'
        )
    

    test_connection(db)
    return db

def test_connection(db):

    cursor = db.cursor()

    cursor.execute("SELECT VERSION()")

    results = cursor.fetchone()

    if not results:
        raise Exception('database broke')

    return True

def get_launch_id(db, description):
    """ launch id is the auto incrementing foreign key to relate and find launches, it is create when
    you call `usp_AddLaunch(descr VARCHAR(250))`"""
    cursor = db.cursor()
    sql_str = 'SELECT max(l_id) FROM LAUNCH WHERE l_description = ' + wrap_quotes(description) + ';'
    print('sql_str: ', sql_str)
    launch_id = cursor.execute(sql_str)
    return cursor.fetchone()[0]

def write_rocket(db, launch_id, time_ms):
    t = time_ms * 1000 # physics scaled time or something
    alt = math.sin(t/10000)
    x = (0.00000001) * t +  32.3946993
    y = 0.0001*math.sin(t/10000) - 106.4729961
    dx = 0.0001
    dy = math.cos(t/10000)
    speed = (dx**2+dy**2)**0.5
    separation = int(alt > 0.5) # 1 or 0 based on altitude

    # 10% packet loss rate just for fun
    if random.randint(0, 10) != 0:
        proc_call(db, 'usp_AddTelemetry_Nosecone', launch_id, time_ms, alt, alt, speed, x, y,
                  2.7*random.random(), 100*random.random(), separation, random.random())

    x = (0.00000001) * t +  32.3946993
    y = 0.0001*math.sin(-t/10000) - 106.4729961
    dx = 0.0001
    dy = math.cos(-t/10000)
    speed = (dx**2+dy**2)**0.5

    proc_call(db, 'usp_AddTelemetry_Vehicle', launch_id, time_ms, alt, speed, 0, x, y, 
              2.7*random.random(), 100*random.random(), separation, random.random())

def wrap_quotes(string):
    return '"' + string + '"'

def proc_call(db, name, *args):
    """ Call sigs for all the functions we have:

    usp_AddTelemetry_Nosecone(launchID INT, timeoftransmission FLOAT, altitude FLOAT, 
        GPSaltitude FLOAT, GPSspeed FLOAT, GPSx FLOAT, GPSy FLOAT, battery FLOAT, 
        temperature FLOAT, separation TINYINT, signalStrength INT)

    usp_AddTelemetry_Vehicle(launchID INT, timeoftransmission FLOAT, altitutde FLOAT, 
        speed FLOAT, acceleration FLOAT, GPSx FLOAT, GPSy FLOAT, voltage FLOAT,
        temperature FLOAT, separation TINYINT(4), signalStrength INT)

    usp_AddLaunch(descr VARCHAR(250))
    """

    # python is the magic glue between everything!
    args = [wrap_quotes(x) if (type(x) is str) else str(x) for x in args]
    sql_str = 'CALL ' + name +  '(' + ', '.join(args) + ');'

    cursor = db.cursor()
    print('executing sql: ', sql_str)
    cursor.execute(sql_str)
    db.commit()

def launch_forever():
    'only put this in a function because I am too weak to use the global namespace'
    time_ms_start = time.time()

    # connect and raise error if not able to connect
    db = connect_database("127.0.0.1")
    test_connection(db)

    desc = 'simulated_launch_' + str(random.randint(1000, 9999))
    proc_call(db, 'usp_AddLaunch', desc)
    launch_id = get_launch_id(db, desc)
    print(desc, 'launch_id = ', launch_id)

    # write launch id so server knows what it is ;)
    open('LAUNCH_ID', 'w').write(str(launch_id))

    
    while True:
        time_ms = time.time() - time_ms_start
        print(time_ms)
        write_rocket(db, launch_id, time_ms)
        time.sleep(2)

if __name__ == '__main__':
    launch_forever()
