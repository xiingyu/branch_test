import serial
import time

header1 = 0xFF
header2 = 0xFE
motor_id = 0x00
datasize = 0x07
mode = 0x01
direction = 0x00
position1 = 0x46
position2 = 0x50
velocity1 = 0x00
velocity2 = 0x32

checksum = (~(motor_id + datasize + mode + direction + position1 + position2 + velocity1 + velocity2)&0xFF)

data_array = bytes([header1, header2, motor_id, datasize, checksum, mode, direction, position1, position2, velocity1, velocity2])
reset_array = bytes([0xFF, 0xFE, 0x00, 0x02, 0xF0, 0x0D])

def main() :
    header1 = 0xFF
    header2 = 0xFE
    motor_id = 0x00
    datasize = 0x07
    mode = 0x01
    direction = 0x00
    position1 = 0x46
    position2 = 0x50
    velocity1 = 0x00
    velocity2 = 0x32
    
    ser = serial.Serial('/dev/ttyUSB0',9600, timeout = 5) 
    
    while True :

        checksum = (~(motor_id + datasize + mode + direction + position1 + position2 + velocity1 + velocity2)&0xFF)
        data_array = bytes([header1, header2, motor_id, datasize, checksum, mode, direction, position1, position2, velocity1, velocity2])  
        
        
        for data in data_array :
            ser.write(data.to_bytes(1, byteorder='big'))
        
        time.sleep(1)
        position2+=0x20


if __name__ == "__main__" :
    main()