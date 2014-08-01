#!/usr/bin/env python

import struct
import sys
import socket
from time import sleep
import rospy
from robucar.srv import RobotCtrl

class Control(object):
	"""docstring for Robucar"""
	def __init__(self):
		super(Control, self).__init__()
		HOST = '10.1.40.56'
		PORT = 8010
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		a = self.conn.connect_ex((HOST, PORT))
		while a!=0:
			print "reconecting in 5\n"  
			sleep(5)
			a = self.conn.connect_ex((HOST, PORT))

	def close(self):
		self.conn.close()

	def __del__(self) :

		""" override the default destructor """
		self.close()
		print "RobuPy stopped, socket closed"

	def sendCommand(self,req):
		ctrl_def = "<dddhhhh"
		data = struct.pack(ctrl_def, 
						   float (req.speed         ),
						   float (req.angle_forward ),
						   float (req.angle_rear    ),
						   int   (req.position_tilt ),
						   int   (req.position_pan  ),
						   int   (req.speed_pan     ),
						   int   (req.speed_tilt    ))
		self.conn.send(data)
		return True


if __name__ == '__main__':

	c = Control()
	sleep(1)

	rospy.init_node('robucar_ctrl', anonymous=True)
	s = rospy.Service('robu_control', RobotCtrl, c.sendCommand)
	print "robucar ready to receive commends"
	rospy.spin()