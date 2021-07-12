import serial
import time

#ser = serial.Serial('/dev/ttyACM2', 9600, timeout=1)
ser = serial.Serial('COM5', 9600, timeout=1)
ser.flush()

def send_comm(comm):
        what = comm
        ser.write(what.encode())
        time.sleep(1)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)