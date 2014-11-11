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
    import serial, time
    t0 = time.time()
    ser = serial.Serial('/dev/tty.usbmodem14531', 115200)
    t1 = time.time()
    time.sleep(0.10)
    print "time taken was: ",t1-t0
    switch_vacuum(ser,1)
    time.sleep(5)
    switch_vacuum(ser,0)
    
    
    
    
