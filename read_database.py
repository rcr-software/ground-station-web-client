import math
import json
import time
import random
import datetime

import mysql.connector

# copy pasted verbatim, would use a local import if I 
# was truly the hero they needed.
def connect_database():
    db = mysql.connector.connect(
            host='127.0.0.1',
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

def get_max_launch_id(db):
    cursor = db.cursor()
    cursor.execute('SELECT MAX(l_id) FROM LAUNCH;')
    lid =  cursor.fetchone()[0]
    db.commit()
    return lid


def read_rocket(db, launch_id, last_tn_id, last_tv_id):
    " time start and end should be in seconds, floats are allowed"
    cursor = db.cursor()

    # nosecone data
    nosecone_str =  f' select * from TELEMETRY_NOSECONE where tn_lid = {launch_id} AND tn_id > {last_tn_id};'
    print('\n', nosecone_str)
    cursor.execute(nosecone_str)
    nosecone_data = list(cursor.fetchall())

    # vehicle data
    vehicle_str = f'select * from TELEMETRY_VEHICLE where tv_lid = {launch_id} AND tv_id > {last_tv_id};'
    print(vehicle_str)
    cursor.execute(vehicle_str)
    vehicle_data = list(cursor.fetchall())
    
    print(nosecone_data)

    # get max tn and tv ids and send em' back to make it easier on the javscript
    cursor.execute('select MAX(tn_id) from TELEMETRY_NOSECONE;')
    max_tn_id = cursor.fetchone()[0]
    cursor.execute('select MAX(tv_id) from TELEMETRY_VEHICLE;')
    max_tv_id = cursor.fetchone()[0]

    nosecone_column_names = ['tn_id', 'tn_lid', 'tn_timestamp', 'tn_timeoftransmission', 'tn_altitude',
        'tn_GPSaltitude', 'tn_GPSspeed', 'tn_GPSx', 'tn_GPSy', 'tn_batteryvoltage', 'tn_internaltemp', 'tn_separation',
        'tn_signal'] 
    vehicle_column_names = ['tv_id', 'tv_lid', 'tv_timestamp', 'tv_timeoftransmission', 'tv_altitude', 'tv_speed',
        'tv_acceleration', 'tv_GPSx', 'tv_GPSy', 'tv_batteryvoltage', 'tv_internaltemp', 'tv_separation', 'tv_signal']

    db.commit() # don't forget to commit or it wont update


    return (nosecone_data,  vehicle_data, max_tn_id, max_tv_id)
