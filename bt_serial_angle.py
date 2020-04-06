import serial
import math 
  
ser = serial.Serial('/dev/ttyUSB0')

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
    #x = ser.read()          # read one byte
    #s = ser.read(10)        # read up to ten bytes (timeout)
    while (True):
        line = ser.readline()   # read a '\n' terminated line
        if "$CSIMU" in str(line): 
            line = str(line).split(',')
            temp = [float(line[2]), float(line[3]), float(line[4])]
            
            x_Buff = temp[0]
            y_Buff = temp[1]
            z_Buff = temp[2]
            
            roll = math.atan2(y_Buff , z_Buff) * 57.3
            pitch = math.atan2((- x_Buff) , math.sqrt(y_Buff * y_Buff + z_Buff * z_Buff)) * 57.3

            print(round(roll,1), round(pitch,1))

            