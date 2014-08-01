#!/usr/bin/env python

import sys
import rospy
from time import sleep
from robucar.srv import RobotCtrl
from robucar.srv import RobotDrive
from robucar.srv import RobotPTU
from robucar.msg import RobotData
        

def drive(speed, fangle, rangle):
    rospy.wait_for_service('robu_control')
    try:
        robu_serve = rospy.ServiceProxy('robu_control', RobotCtrl)
        resp1 = robu_serve(speed, fangle, rangle,1,2,3,4)
        return resp1.retval
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        return resp1.retval

def adrive(speed, fangle, rangle):
    print "this"
    rospy.wait_for_service('robu_Drive')
    sleep(0.5)
    x = 0
    try:
        robu_serve = rospy.ServiceProxy('robu_Drive', RobotDrive)
        while x <= speed:
            resp1 = robu_serve(x, fangle, rangle)
            if speed > 0:
                x += .1
            else:
                x -= .1
            sleep(.2)
        return resp1.retval
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        return resp1.retval

def usage():
    return "%s [speed fangle rangle]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        speed =  float(sys.argv[1])
        fangle = float(sys.argv[2])
        rangle = float(sys.argv[3])
    else:
        print usage()
        sys.exit(1)
    print "Sending %s , %s , %s"%(speed, fangle, rangle)
    print "%s"%(adrive(speed, fangle, rangle))
