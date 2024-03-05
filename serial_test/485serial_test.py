
import serial



def main():
    direction = 0x56

    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
    ser.write(direction.to_bytes(1, byteorder='big'))

if __name__ == '__main__':
    main()