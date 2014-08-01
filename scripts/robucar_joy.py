#!/usr/bin/env python

import sys
import rospy
from time import sleep
from robucar.srv import RobotCtrl
from robucar.srv import RobotDrive
from robucar.srv import RobotPTU
from robucar.msg import RobotData
from sensor_msgs.msg import Joy
     
class Robot(object):
	def __init__(self):
		self.speed = 0.0
		self.df = False
		self.db = False
		self.fangle = 0.0
	

	def inc(self):
		if self.speed == 2:
			print "max speed 2"
		else:		
			self.speed +=0.5
	def dec(self):
		if self.speed == 0:
			print "min speed 0"
		else:		
			self.speed -=0.5

	def drive(self,s, f, r):
		rospy.wait_for_service('robu_Drive')
		try:
			robu_serve = rospy.ServiceProxy('robu_Drive', RobotDrive)
			resp1 = robu_serve(s,f,r)
			return resp1.retval
		except rospy.ServiceException, e:
			print "Service call failed: %s"%e
			return resp1.retval	   

	def joyCallback(self, data):

		if data.axes[6] == 1.0:
			print "up"
			self.df = True
		else:	
			self.df = False

		if data.axes[6] == -1.0:
			print "down"
			self.db = True
		else:	
			self.db = False

		if data.axes[5] == 1.0:
			print "left"
			self.fangle = -15.0
		elif data.axes[5] == -1.0:
			print "right"
			self.fangle = 15.0
		else:	
			self.fangle = 0.0

		if data.buttons[0] == 1:
			print "r up"
		if data.buttons[2] == 1:
			print "r down"
		if data.buttons[3] == 1:
			print "r left"
		if data.buttons[1] == 1:
			print "r right"

		if data.buttons[5] == 1:
			self.inc()
			print "increase speed", self.speed
		if data.buttons[7] == 1:
			self.dec()
			print "decrease speed", self.speed

		self.drive(self.speed, self.fangle, 0.0 )




if __name__ == "__main__":
	r = Robot()
	rospy.init_node('robucar_joy', anonymous=True)
	#rospy.Subscriber('robot_data', RobotData, c.rdata.update)
	rospy.Subscriber('joy', Joy, r.joyCallback)
	rospy.spin()
    