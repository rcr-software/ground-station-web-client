import mysql.connector

def connect_to_database(host):
    db = mysql.connector.connect(
            host=host,
            db="GCDB",
            user="webuser",
            passwd="password"
        )

    return db

def test_connection(con):

    cursor = con.cursor()

    cursor.execute("SELECT VERSION()")

    results = cursor.fetchone()

    if results:
        return True
    else:
        return False


def exec_query(con, query):
    if(con == None):
        return

    cursor = con.cursor()

    cursor.execute(query)

    for x in cursor:
        print(x)

def get_launch_id(con, desc):
    db_cursor = con.cursor()

    launch_id = db_cursor.execute("SELECT max(l_id) FROM LAUNCH WHERE l_description = \"" + desc + "\"")

    for x in db_cursor:
        return x[0]

def load_launch_id(con):
    db_cursor = con.cursor()

    user_in = input("Enter Launch ID: ")
    db_cursor.execute("SELECT l_id FROM LAUNCH WHERE l_id = "+user_in)

    for x in db_cursor:
        return x[0]

    return 0;


def instert_into_launch(con, separation, end, desc):
    sql_string = "CALL usp_Add_launch( NOW(), "+ separation+", "+ end+", \""+desc+"\")"

    db_cursor = con.cursor()
    db_cursor.execute(sql_string)
    con.commit()

    launch_id = get_launch_id(con, desc)

    return launch_id

def insert_into_telemetry_nosecone(con, launch_id, GPSx, GPSy, altitude):
    sql_string = "CALL usp_AddTelemetry_Nosecone( "+str(launch_id)+", "+GPSx+", "+GPSy+", "+altitude+")"

    db_cursor = con.cursor()
    db_cursor.execute(sql_string)
    con.commit()

def insert_into_telemetry_vehicle(con, launch_id, velocity, GPSx, GPSy, altitude, voltage, temp):
    sql_string = "CALL usp_Add_telemetry_Vehicle( "+str(launch_id)+", "+velocity+", "+GPSx+", "+GPSy+", "+altitude+", "+voltage+", "+temp+")"

    db_cursor = con.cursor()
    db_cursor.execute(sql_string)
    con.commit()

def Main():
    IP = "192.168.0.101"
    LAUNCH_ID = 0

    print("River City Rocketry");
    print("Ground Computer Database Client")
    print("Written by: Tom Sarver")

    user_in = -1

    while(user_in != "0"):
        print("\n1) Set Connection Variables")
        print("2) Get Connection Variables")
        print("3) Test Database Connection")
        print("4) Query Database")
        print("5) New Launch")
        print("6) Load Launch")
        print("t) Execute Test Function")
        print("0) Exit")

        user_in = input("Option: ")
        if(user_in == "t"):
            testfxn()
        elif(user_in == "1"):
            option = input("Use Default Connection?(y/n): ")
            if(option.upper() == "Y"):
                IP = "192.168.0.101"
            else:
                user_ip = input("Host IP: ")
                IP = user_ip
        elif(user_in == "2"):
            print("\nHost: "+IP)
            print("Database: GCDB")
            print("User: webuser")

            print("\nLaunch ID: "+str(LAUNCH_ID))

        elif(user_in == "3"):
            test = test_connection(connect_to_database(IP))

            if(test == True):
                print("\nConnection Succeeded")
            else:
                print("\nConnection Failed")
        elif(user_in == "4"):
            q = input("db> ")

            db = connect_to_database(IP)

            exec_query(db, q)
        elif(user_in == "5"):
            desc = input("Launch Description: ")

            db = connect_to_database(IP)
            LAUNCH_ID = instert_into_launch(db, "NULL", "NULL", desc)
        elif(user_in == "6"):
            db = connect_to_database(IP)

            LAUNCH_ID = load_launch_id(db)

def testfxn():
    IP = "192.168.1.126"
    LAUNCH_ID = 0

    print("New Launch")

    db = connect_to_database(IP)

    desc = input("Launch Description: ")
    LAUNCH_ID = instert_into_launch(db, "NULL", "NULL", desc)
    print("LAUNCH_ID: "+str(LAUNCH_ID))

    #Insert Dummy Data
    insert_into_telemetry_nosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    insert_into_telemetry_nosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    insert_into_telemetry_nosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    insert_into_telemetry_nosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")
    insert_into_telemetry_nosecone(db, LAUNCH_ID, "0.0", "0.0", "0.0")

    insert_into_telemetry_vehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    insert_into_telemetry_vehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    insert_into_telemetry_vehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    insert_into_telemetry_vehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")
    insert_into_telemetry_vehicle(db, LAUNCH_ID, "0.0", "0.0", "0.0", "0.0", "0.0", "0.0")

Main()
#testfxn()
