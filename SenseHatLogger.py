# SenseHat-Logger
# Creates a log file for all sensehat sensors
##### Libraries #####
from datetime import datetime
from sense_hat import SenseHat
#from time import sleep
import time
import sys
import os
from threading import Thread

##### Logging Settings #####
FILENAME = ""
LOGNAME = "SenseHat"
WRITE_FREQUENCY = 1
TEMP_H=True
TEMP_P=True
HUMIDITY=True
PRESSURE=True
ORIENTATION=True
ACCELERATION=True
MAG=True
GYRO=True
DELAY=1

##### Functions #####
def file_setup(filename):
    header =[]
    header.append("timestamp")

    if TEMP_H:
        header.append("temp_h")
    if TEMP_P:
        header.append("temp_p")
    if HUMIDITY:
        header.append("humidity")
    if PRESSURE:
        header.append("pressure")
    if ORIENTATION:
        header.extend(["pitch","roll","yaw"])
    if MAG:
        header.extend(["mag_x","mag_y","mag_z"])
    if ACCELERATION:
        header.extend(["accel_x","accel_y","accel_z"])
    if GYRO:
        header.extend(["gyro_x","gyro_y","gyro_z"])

    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in header)+ "\n")

def log_data():
    output_string = ",".join(str(value) for value in sense_data)
    batch_data.append(output_string)


def get_sense_data():
    sense_data=[]

    sense_data.append(time.time())
    
    if TEMP_H:
        sense_data.append(sense.get_temperature_from_humidity())

    if TEMP_P:
        sense_data.append(sense.get_temperature_from_pressure())

    if HUMIDITY:
        sense_data.append(sense.get_humidity())

    if PRESSURE:
        sense_data.append(sense.get_pressure())

    if ORIENTATION:
        o = sense.get_orientation()
        yaw = o["yaw"]
        pitch = o["pitch"]
        roll = o["roll"]
        sense_data.extend([pitch,roll,yaw])

    if MAG:
        mag = sense.get_compass_raw()
        mag_x = mag["x"]
        mag_y = mag["y"]
        mag_z = mag["z"]
        sense_data.extend([mag_x,mag_y,mag_z])

    if ACCELERATION:
        acc = sense.get_accelerometer_raw()
        x = acc["x"]
        y = acc["y"]
        z = acc["z"]
        sense_data.extend([x,y,z])

    if GYRO:
        gyro = sense.get_gyroscope_raw()
        gyro_x = gyro["x"]
        gyro_y = gyro["y"]
        gyro_z = gyro["z"]
        sense_data.extend([gyro_x,gyro_y,gyro_z])

    sense_data.append(datetime.now())

    return sense_data

def timed_log():
    while True:
        log_data()
        sleep(DELAY)




##### Main Program #####
if __name__=="__main__":
    sense = SenseHat()
    batch_data= []

    if len(sys.argv)>1:
        path= sys.argv[1]
        filename = sys.argv[1]+"-"+str(datetime.now())+".csv"
    else:
        filename = os.path.dirname(__file__) + "/" + LOGNAME + str(datetime.now())+".csv"
        
    file_setup(filename)

    if DELAY > 0:
        sense_data = get_sense_data()
        Thread(target= timed_log).start()

    while True:
        sense_data = get_sense_data()

        if DELAY == 0:
            log_data()

        if len(batch_data) >= WRITE_FREQUENCY:
            # print("Writing to file..")
            with open(filename,"a") as f:
                for line in batch_data:
                    f.write(line + "\n")
                    print(line)
                batch_data = []
