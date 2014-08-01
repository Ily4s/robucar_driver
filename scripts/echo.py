#!/usr/bin/env python

import struct
import sys
import socket
from time import sleep
import rospy
from robucar.msg import RobotData


class Rdata(object):
	"""docstring for Rdata"""
	def __init__(self):
		self.speed_average = 0.0
		self.speed_FL      = 0.0
		self.speed_FR      = 0.0
		self.speed_RL      = 0.0
		self.speed_RR      = 0.0
		self.angle_forward = 0.0
		self.angle_rear    = 0.0
		self.position_pan  = 0  
		self.position_tilt = 0  
		self.speed_pan     = 0  
		self.speed_tilt    = 0  

	def update(self, data):
		self.speed_average =  data.speed_average
		self.speed_FL      =  data.speed_FL     
		self.speed_FR      =  data.speed_FR     
		self.speed_RL      =  data.speed_RL     
		self.speed_RR      =  data.speed_RR     
		self.angle_forward =  data.angle_forward
		self.angle_rear    =  data.angle_rear   
		self.position_pan  =  data.position_pan 
		self.position_tilt =  data.position_tilt
		self.speed_pan     =  data.speed_pan    
		self.speed_tilt    =  data.speed_tilt   


if __name__ == '__main__':
	rdata = Rdata()
	sleep(1)
	rospy.init_node('robucar_echo', anonymous=True)
	rospy.Subscriber('robot_data', RobotData, rdata.update)
	while 1:
		print(rdata.speed_average ,rdata.speed_FL      ,rdata.speed_FR      ,rdata.speed_RL      ,rdata.speed_RR      ,rdata.angle_forward ,rdata.angle_rear    ,rdata.position_pan  ,rdata.position_tilt ,rdata.speed_pan     ,rdata.speed_tilt ) 
		sleep(0.5)
	rospy.spin()