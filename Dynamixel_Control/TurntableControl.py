from lib_robotis import *
from usbscan import *
from math import pi

# rpm = angvel * (30/pi)

def setSpeedRPM(rpm):
    "Sets the Dynamixel in wheel mode and the rotational speed to the desired RPM. The RPM is limited by the torque the Dynamixel provides i.e. if the torque is too small the table won't turn. Min RPM = 4.77 & Max RPM = 113.5."
    # Mac: scan_for_usb() only works on a Mac.
    # Windows: set dev_name to the com port of the Dynamixel.
    dev_name = scan_for_usb()
    dyn = USB2Dynamixel_Device(dev_name)

    # the number is the servo ID
    servo = Robotis_Servo(dyn, 1)

    # enable wheel mode
    servo.enable_rotation()

    # angvel limits are:
    # 0.5 - 11.89 --> CCW (tested)
    # 12.5 - 23.7 --> CW (tested)
    # (smaller = slower)
    servo.set_angvel(rpm * (pi/30))
    return

def setSpeedRad(rad):
    "Sets the Dynamixel in wheel mode and the rotational speed to the desired Rad/s. The Rad/s is limited by the torque the Dynamixel provides i.e. if the torque is too small the table won't turn. Min Rad/s = 0.5 & Max Rad/s = 11.89."
    # Mac: scan_for_usb() only works on a Mac.
    # Windows: set dev_name to the com port of the Dynamixel.
    dev_name = scan_for_usb()
    dyn = USB2Dynamixel_Device(dev_name)

    # the number is the servo ID
    servo = Robotis_Servo(dyn, 1)

    # enable wheel mode
    servo.enable_rotation()

    # angvel limits are:
    # 0.5 - 11.89 --> CCW (tested)
    # 12.5 - 23.7 --> CW (tested)
    # (smaller = slower)
    servo.set_angvel(rad)
    return
