#!/usr/bin/env python

import struct
import sys
import socket
from time import sleep
import rospy
from robucar.msg import RobotData


class Monitoring(object):

	"""docstring for Monitoring"""

	def __init__(self):
		super(Monitoring, self).__init__()
		HOST = '10.1.40.98'
		PORT = 8000               
		self.s = None
		self.data = ''

		for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa = res
			try:
				self.s = socket.socket(af, socktype, proto)
			except socket.error, msg:
				self.s = None
				continue
			try:
				self.s.bind(sa)
				self.s.listen(1)
			except socket.error, msg:
				self.s.close()
				self.s = None
				continue
			break
		if self.s is None:
			print 'could not open socket'
			sys.exit(1)

		self.conn, addr = self.s.accept()
		print 'Connected by', addr
		print "Serving at port 8000"
				

	def monitor(self):
		ctrl_def = "<dddddddhhhh"
		pub = rospy.Publisher('robot_data', RobotData, queue_size=10)
		rospy.init_node('robucar_mon', anonymous=True)
		#r = rospy.Rate(10) # 10hz
		while not rospy.is_shutdown():
			buf = self.conn.recv(struct.calcsize(ctrl_def))
			self.data = struct.unpack(ctrl_def, buf)
			#rospy.loginfo(str)
			pub.publish(self.data[0] ,
						self.data[1] ,
						self.data[2] ,
						self.data[3] ,
						self.data[4] ,
						self.data[5] ,
						self.data[6] ,
						self.data[7] ,
						self.data[8] ,
						self.data[9] ,
						self.data[10])
			#r.sleep()

	def close(self):
		self.conn.close()

	def __del__(self):
		""" override the default destructor """
		self.close()
		print "RobuPy stopped, socket closed"


if __name__ == '__main__':
	
	print "starting monitoring server"
	m = Monitoring()
	sleep(1)
	print "begin publishing"
	try:
		m.monitor()
	except rospy.ROSInterruptException: pass