#!/usr/bin/env python

import struct
import sys
import socket
from time import sleep
import rospy
from robucar.srv import RobotDrive
from robucar.srv import RobotPTU
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
		
class Control(object):
	"""docstring for Robucar"""
	def __init__(self):
		super(Control, self).__init__()

		self.rdata = Rdata()
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

	def DriveCommand(self,req):
		ctrl_def = "<dddhhhh"
		self.rdata.speed_average = req.speed
		self.rdata.angle_forward = req.angle_forward
		self.rdata.angle_rear    = req.angle_rear   
		data = struct.pack(ctrl_def, 
						   float (req.speed                ),
						   float (req.angle_forward        ),
						   float (req.angle_rear           ),
						   int   (self.rdata.position_tilt ),
						   int   (self.rdata.position_pan  ),
						   int   (self.rdata.speed_pan     ),
						   int   (self.rdata.speed_tilt    ))
		try:
			self.conn.send(data)
			return True
		except:
			return False
		

	def PTUCommand(self,req):
		ctrl_def = "<dddhhhh"
		self.rdata.position_tilt = req.position_tilt
		self.rdata.position_pan  = req.position_pan 
		self.rdata.speed_pan     = req.speed_pan    
		self.rdata.speed_tilt    = req.speed_tilt   
		data = struct.pack(ctrl_def, 
						   float (self.rdata.speed_average ),
						   float (self.rdata.angle_forward ),
						   float (self.rdata.angle_rear    ),
						   int   (req.position_tilt        ),
						   int   (req.position_pan         ),
						   int   (req.speed_pan            ),
						   int   (req.speed_tilt           ))
		try:
			self.conn.send(data)
			return True
		except:
			return False




if __name__ == '__main__':

	c = Control()
	sleep(1)
	rospy.init_node('robucar_ctrl', anonymous=True)
	rospy.Subscriber('robot_data', RobotData, c.rdata.update)
	sleep(1)
	s = rospy.Service('robu_PTU', RobotPTU, c.PTUCommand)
	s = rospy.Service('robu_Drive', RobotDrive, c.DriveCommand)
	print "robucar ready to receive commends"
	rospy.spin()