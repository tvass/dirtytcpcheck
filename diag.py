#!/usr/bin/env python
#
# netdiag.py is a dirty TCP connexion checker
# using a static list.
#
# By running this script on different servers
# located in several datacenters/country you can
# quickly expose routing or filtering issues on 
# your network ...
# 
# Input format is compliant with a basic "database export"
# like csv ...
#
# hostnamex,ip x,21,22,80.443
# hostnamey,ip y,80,139,445
#
# Output is grep'able (with ^OK or ^KO)
#
# Ps : Adjust timeout to fit your needs.
#
# A+
# Thom

import socket
import sys

class host:
	def __init__(self):
        	self.name = None
                self.ip = None
                self.ports = []

class test_tcp:
	def  __init__(self, port):
		self.port = port
	def run(self, host):
		s = socket.socket()
		s.settimeout(2)
		try:
                                s.connect((host, self.port))
				return True
		except socket.error, e:
				return False
		s.close()

if __name__ == '__main__':
	ins = open( "list.txt", "r" )
	for line in ins:
		array = line.split(',')
		
		myhost = host()
		myhost.name = array[0]
		myhost.ip = array[1]
		ports =  array[2:]
		for port in ports:
			myhost.ports.append(int(port))
		
		for port in myhost.ports:
			mytest = test_tcp(port)
			if mytest.run(myhost.ip):
				print "OK", repr(myhost.name).ljust(30), repr(myhost.ip).ljust(15), repr(port).rjust(2)
			else:
				print "KO", repr(myhost.name).ljust(30), repr(myhost.ip).ljust(15), repr(port).rjust(2)
	ins.close()
