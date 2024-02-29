import serial
import os
import time

# 시리얼 포트 경로 및 전송 속도 설정
port = "/dev/ttyS1"
baud_rate = 9600

def open_port(port, baud_rate):
    # 시리얼 포트에 액세스 가능한지 확인
    if not os.path.exists(port):
        print(f"Can't access port: {port}, exit node lidar.")
        return None
    
    # 시리얼 포트 열기
    ser = serial.Serial(port, baud_rate, timeout=0)
    
    # 시리얼 포트 설정 확인
    if ser.isOpen():
        print("open_port ok.")
    else:
        print("Can't Open SerialPort")
        return None
    
    return ser

def read_port(ser, len):
    # 시리얼 포트로부터 데이터 읽기
    try:
        data = ser.read(len)
        return data
    except serial.SerialException as e:
        print("Serial Port Exception:", e)
        return None

def write_port(ser, data):
    # 시리얼 포트에 데이터 쓰기
    try:
        return ser.write(data)
    except serial.SerialException as e:
        print("Serial Port Exception:", e)
        return None

def close_port(ser):
    # 시리얼 포트 닫기
    try:
        ser.close()
        print("Serial port closed.")
    except serial.SerialException as e:
        print("Serial Port Exception:", e)

def main():
    # 시리얼 포트 열기
    ser = open_port(port, baud_rate)
    if ser is None:
        return

    try:
        # 시리얼 포트로부터 데이터 읽기 예제
        data = read_port(ser, 10)
        if data is not None:
            print("Read data:", data)
        
        # 시리얼 포트에 데이터 쓰기 예제
        write_data = b"Hello, world!"
        write_port(ser, write_data)
        print("Data written to serial port.")
        
    finally:
        # 시리얼 포트 닫기
        close_port(ser)

if __name__ == "__main__":
    main()
