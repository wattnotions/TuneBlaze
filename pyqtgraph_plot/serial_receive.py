import serial
 
ser = serial.Serial(
    port='COM6',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None
)
 
ser.close()
ser.open()
print (ser.isOpen())


print("Waiting for data....")

while(True):
    data = ser.readline()
    split_data = data.decode().split(',')
    print(len(split_data))
    




print("Exiting Program")
        