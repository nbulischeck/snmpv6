#!/usr/bin/env python
import argparse
from socket import gethostbyname
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import cmdgen

addressList = []
linkTypes = ["Loopback:", "Unique Local:", "Link-Local:"]

def getHost(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBindTable, cbCtx):
	if errorIndication:
		print(errorIndication)
		return
	if errorStatus and errorStatus != 2:
		print('Error: %s' % errorStatus.prettyPrint())
		return
	for varBindRow in varBindTable:
		for oid, val in varBindRow:
			if "1.3.6.1.2.1.1.1.0" in oid.prettyPrint():
				print("System Info:\t", val.prettyPrint())
				return
		print("[!] Unable to find system info!")
		return

def getAddrs(snmpEngine, sendRequestHandle, errorIndication,
          errorStatus, errorIndex, varBindTable, cbCtx):
	if errorIndication:
		print(errorIndication)
		return
	if errorStatus and errorStatus != 2:
		print('Error: %s' % errorStatus.prettyPrint())
		return
	for varBindRow in varBindTable:
		for oid, val in varBindRow:
			if "1.3.6.1.2.1.4.34.1.3.2.16" not in oid.prettyPrint():
				return
			else:
				addressList.append(oid.prettyPrint())
	return 1

def createSNMP(host, community=None):
	if community is None:
		community = "public"

	ip = gethostbyname(host)
	snmpEngine = engine.SnmpEngine()
	config.addV1System(snmpEngine, 'my-area', community)
	config.addTargetParams(snmpEngine, 'my-creds', 'my-area', 'noAuthNoPriv', 0)
	config.addTransport(
		snmpEngine,
		udp.domainName,
		udp.UdpSocketTransport().openClientMode()
	)
	config.addTargetAddr(
		snmpEngine, 'my-router',
		udp.domainName, (ip, 161),
		'my-creds'
	)

	cmdgen.NextCommandGenerator().sendVarBinds(
		snmpEngine,
		'my-router',
		None, '',
		[((1, 3, 6, 1, 2, 1, 1, 0, 0), None)],
		getHost
	)
	snmpEngine.transportDispatcher.runDispatcher()

	cmdgen.NextCommandGenerator().sendVarBinds(
		snmpEngine,
		'my-router',
		None, '',
		[((1, 3, 6, 1, 2, 1, 4, 34, 1, 3, 2, 16), None)],
		getAddrs
	)
	snmpEngine.transportDispatcher.runDispatcher()

def main():
	parser = argparse.ArgumentParser(description="Get IPv6 Addresses via SNMP", 
										add_help=False)
	parser.add_argument("--help", action="help")
	required = parser.add_argument_group('required arguments')
	required.add_argument("-h", dest="host",
						help="ip address of the remote host",
						required=True,
						action="store")
	required.add_argument('-c',  dest='community',
                    	help='community (public, private, etc.)',
						required=True,
						action="store")
	args = parser.parse_args()

	if args.host and args.community:
		createSNMP(args.host, args.community)
		if addressList:
			for i, address in enumerate(addressList):
				address = address[len("1.3.6.1.2.1.4.34.1.3.2.16."):].split(".")
				for j, val in enumerate(address):
					address[j] = hex(int(val))[2:]
				t = iter(address)
				address = ':'.join([i+next(t, '') for i in t])
				print(linkTypes[i], "\t", address)
		else:
			print("[!] Unable to find any IPv6 Addresses.")
		
if __name__ == "__main__":
	main()
