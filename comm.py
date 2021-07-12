import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#ser = serial.Serial('COM5', 9600, timeout=1)
ser.flush()

def send_comm(comm):
	ser.write(comm.encode())
	line = ser.readline().decode('utf-8').rstrip()