
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

def distance(*args):
    return sum([x**2 for x in args])**0.5

class PhysicsObject():
    def __init__(self, x, y, z, floor_z):
        self.x = x
        self.y = y
        self.z = z
        self.floor_z = floor_z
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.speed = 0
        self.acceleration = 0

    def copy_from(self, other):
        self.x = other.x
        self.y = other.y
        self.z = other.z
        self.dx = other.dx
        self.dy = other.dy
        self.dz = other.dz
        self.acceleration = 0

    def step(self, additional_dz=0):
        starting_velocity = distance(self.dx, self.dy, self.dz)
        
        self.x += dx
        self.y += dy
        self.z += dz
        if self.z < self.floor_z:
            self.z = self.floor_z
            self.dz = 0

        if self.z - self.floor_z > 100:
            self.dx += 0.001
            self.dy += 0.001

        self.dx += 0.0001 * (random.random() - 0.5)
        self.dy += 0.0001 * (random.random() - 0.5)

        self.dx = self.dx * 0.9
        self.dy = self.dy * 0.9

        self.dz = self.dz - 16 + additional_dz
   
        self.acceleration = distance(self.dx, self.dy, self.dz) - starting_velocity
        self.speed = distance(self.dx, self.dy, self.dz)
 


class Rocket():
    def __init__(self, launch_id):
        self.vehicle = Physics(32.3946993, -106.4729961, 4300.0, 4300.0)
        self.nosecone = Physics(32.3946993, -106.4729961, 4300.0, 4300.0)
        self.launch_id = launch_id
        self.time = time.time() * 1000

        self.fuel = 100
        self.launched = False
        self.seperation = False

        self.temperature = 105.0
        self.acceleration = 0
        self.battery = 3.71
        self.signal_strength = 1

    def write_database(self, db):
        proc_call(db, 'usp_AddTelemetry_Nosecone', self.launch_id, self.time,
            self.nosecone.x, self.nosecone.z, self.nosecone.speed,
            self.nosecone.x, self.nosecone.y, self.battery, self.temperature,
            int(self.seperation), self.signal_strength)
        proc_call(db, 'usp_AddTelemetry_Vehicle', self.launch_id, self.time,
        self.vehicle.z, self.vehicle.z, self.vehicle.speed,
            self.acceleration, self.x, self.y, self.battery,
            self.temperature, int(self.seperation), self.signal_strength]

    def launch(self):
        self.launched = True

    def physics_step(self):

        self.time = time.time() * 1000
        

        if self.seperation:
            self.nosecone.step()
            self.vehicle.step()
        else:
            self.vehicle.step()
            self.nosecone.copy_from(self.vehicle)

        if self.launched and fuel > 0:
            fuel -= 1
            self.vehicle.dz += 300

        if self.dz < -10:
            self.seperation = True
            self.nosecone.seperate()
            
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
    sql_str = name + '(' + ', '.join(args) + ')'

    dbCursor = con.cursor()
    dbCursor.execute(sql_str)
    con.commit()

ip = "127.0.0.1"
launch_id = 1

print("New Launch")

db = ConnectToDatabase(ip)

desc = 'simulated launch ' + str(launch_id)

proc_call(db, 'usp_AddLaunch', desc)
