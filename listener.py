## Simple talker demo that listens to recognized_object_array
## Adapted from the sample ROS listener code 

import rospy
from time import sleep
import serial
import struct
from object_recognition_msgs.msg import RecognizedObjectArray
import serial
import struct
import time

#ser is the serial port address for the solenoid arduino
#ser_two is the serial port address for the arduino attached to the stepper motors

ser = serial.Serial('/dev/cu.usbmodemfd121')
ser_two = serial.Serial('/dev/cu.usbmodemfa131')  # open serial port






def close_left():
    ser.write(struct.pack(">B", 101))
def close_right():
    ser.write(struct.pack(">B", 103))
def open_left():
    ser.write(struct.pack(">B", 102))
def open_right():
    ser.write(struct.pack(">B", 104))
def close_both():
    ser.write(struct.pack(">B", 101))
    ser.write(struct.pack(">B", 103))
def open_both():
    ser.write(struct.pack(">B", 102))
    ser.write(struct.pack(">B", 104))


def turn_left():
    ser_two.write(struct.pack(">B", 105))
def turn_right():
    ser_two.write(struct.pack(">B", 106))

def dump_left():
    close_both()
    time.sleep(3)
    open_left()
    time.sleep(1)
    turn_left()
    turn_left()
    turn_left()
    turn_left()
    time.sleep(3)

    turn_right()
    turn_right()
    turn_right()
    turn_right()


    time.sleep(2)
    turn_right()
    close_both()
    time.sleep(3)
    open_both()

    ser_two.setDTR(False) # Drop DTR
    time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
    ser_two.setDTR(True)  # UP the DTR back


def dump_right():
    close_both()
    time.sleep(3)
    open_right()
    time.sleep(1)
    turn_right()
    turn_right()
    turn_right()
    turn_right()
    time.sleep(3)
    turn_left()
    turn_left()
    turn_left()
    turn_left()


    time.sleep(2)
    turn_left()
    close_both()
    time.sleep(3)
    open_both()
    ser_two.setDTR(False) # Drop DTR
    time.sleep(0.022)    # Read somewhere that 22ms is what the UI does.
    ser_two.setDTR(True)  # UP the DTR back


def test():
    lightLevel = False
    triggered = False
    while not triggered:
        observed = ser.read()
        try:
            observed = int(observed)
        except:
            observed = False
        if observed in [0, 1, 2]:
            lightLevel = int(observed)
        print(lightLevel)
        if lightLevel ==1:
            dump_left()
            time.sleep(5)
            triggered = True
        elif lightLevel == 2:
            dump_right()
            time.sleep(5)
            triggered = True

def other_test():
    dump_left()
    dump_right()







def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", len(data.objects))
    #ser.write(chr(len(data.objects))) # Convert the decimal number to ASCII then send it to the Arduino
    print(data)
    lightLevel = False
    observed = ser.read()
    try:
        observed = int(observed)
    except:
        observed = False
    if observed in [0, 1, 2]:
        lightLevel = int(observed)
    print(lightLevel)
    if lightLevel > 0:
        if len(data.objects):
            dump_left()
            time.sleep(5)
        else:
            dump_right()
            time.sleep(5)

    print "this is what duino sees"


    #print type(ser.readline())
    print 'yep'
def listener():
    triggered = False
    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("recognized_object_array", RecognizedObjectArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()