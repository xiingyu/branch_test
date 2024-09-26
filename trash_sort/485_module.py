import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)
"""
while True :
    if ser.in_waiting > 0:
        # 시리얼로부터 데이터 읽기
        data = ser.read(ser.in_waiting)  # 사용 가능한 데이터만큼 읽음
        
        # 16진수로 변환하여 출력
        hex_data = data.hex()  # 수신한 데이터를 16진수로 변환
        print(f"수신한 데이터 (16진수): {hex_data}")
        
    else :
        in_data = input("input tx data : ")
        
        hex = int(in_data,16)
        # ser.write(hex)
        ser.write(hex.to_bytes(1, byteorder='big'))  # 1바이트로 변환 후 전송
    
    # time.sleep(2)
    # ser.write(b'a')        
    # ser.write('0xa'.encode())
    # ser.write(bytes([0xAA]))
        print(f'send {hex}')
  

# while True :
    
#     time.sleep(2)
#     # ser.write(b'a')        
#     # ser.write('0xa'.encode())
#     ser.write(bytes([0xAF]))

"""
try:
    while True:
        if ser.in_waiting > 0:
            # 시리얼로부터 데이터 읽기
            data = ser.read(ser.in_waiting)  # 사용 가능한 데이터만큼 읽음
            
            # 16진수로 변환하여 출력
            hex_data = data.hex()  # 수신한 데이터를 16진수로 변환
            print(f"수신한 데이터 (16진수): {hex_data}")

except KeyboardInterrupt:
    print("종료...")

finally:
    ser.close()  # 프로그램 종료 시 시리얼 포트 닫기
