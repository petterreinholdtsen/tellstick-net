#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Telldus Technologies AB. All rights reserved.
#
# Copyright: See COPYING file that comes with this distribution
#
#

import socket, sys

UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
UDPSock.setblocking(1)
UDPSock.settimeout(3)

UDPSock.bind( ('', 42314) )

print "Autodiscover TellStick Net..."
UDPSock.sendto("D", ('255.255.255.255',30303))

ip = None

while 1:
	try:
		(buf, (ip, port)) = UDPSock.recvfrom(2048)
	except socket.error, msg:
		break
	m = buf.split(':')
	print("Found %s on ip %s firmware version %s" % (m[0], ip, m[3]))
	if (m[3] == 'X' or 17 <= int(m[3])):
		print("  This has firmware %s, lets use it" % m[3])
		break
	else:
		print "  Not using correct firmware"
	ip = None

if (ip == None):
	print "No TellStick Net with correct firmware found"
	sys.exit(1)

print "Send Arctech selflearning turn on to %s" % ip

protocol = 'arctech'
model = 'selflearning'
house = 53103098
unit = 0
method = 2
msg = "4:sendh8:protocol%X:%s5:model%X:%s5:housei%Xs4:uniti%Xs6:methodi%Xss" % (len(protocol), protocol, len(model), model, house, unit, method)

UDPSock.sendto(msg,(ip,42314))
sys.exit(0)
