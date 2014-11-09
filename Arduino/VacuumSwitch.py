"Switch the vacuum on and off"

def init_arduino():
    import serial, time
    ser = serial.Serial('/dev/tty.usbmodem14531', 115200)
    return ser

def switch_vacuum(ser,state):
    
    if state == 1:
        ser.write('o')
    elif state == 0:
        ser.write('x')
    else:
        return

if __name__ == '__main__':
    import time
    ser = init_arduino()
    switch_vacuum(ser,1)
    time.sleep(5)
    switch_vacuum(ser,0)
    
    
    
    
