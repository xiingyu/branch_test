import serial

ser = serial.Serial('dev/ttyS0', 4800, timeout=0.01)

def TX(data) :
    ser.write(serial.to_bytes([data]))
    return

def RX() :
    if serial.inWaiting() > 0 :
        result = ser.read(1)
        RX = ord(result)
        return RX
    else :  
        return 0

def main() :
    while True :
        cmd_val = int(input("input UR command : "))
        
        TX(cmd_val)
        result = RX()
        
        print(result)
        
        

if __name__ == "__main__" :
    main()