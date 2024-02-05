import serial
import time



def main() :
    header1 = 0xFF
    header2 = 0xFE
    motor_id = 0x00
    datasize = 0x06
    mode = 0x03
    direction = 0x01
    velocity1 = 0x00
    velocity2 = 0x64
    duration = 0x0A
    
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 5) 
    
    while True :

        checksum = (~(motor_id + datasize + mode + direction + velocity1 + velocity2 + duration)&0xFF)
        data_array = bytes([header1, header2, motor_id, datasize, checksum, mode, direction, velocity1, velocity2, duration])  
        
        
        for data in data_array :
            ser.write(data.to_bytes(1, byteorder='big'))


if __name__ == "__main__" :
    main()