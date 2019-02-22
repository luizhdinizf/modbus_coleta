import pymodbus
import serial
import os
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.transaction import ModbusRtuFramer

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


from pymodbus.compat import iteritems
from collections import OrderedDict
import subprocess
import time
import json
import datetime
def check(cmd):
	while 'tty' not in os.listdir('/home/pi'):
		subprocess.call('pkill socat',shell=True)
		time.sleep(1)
		subprocess.Popen(cmd,shell=True)
		print('nao abriu')
		time.sleep(1)
	return
	

cmd = "socat pty,link=/home/pi/tty,raw tcp:192.168.4.232:4660"
print("start.....")

time.sleep(50)
check(cmd)
	
print ('abriu')

	
print("starting")

#import logging
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from
addresses = [1,2,3,4,5,6]
client= ModbusClient(method = "rtu", port="/home/pi/tty",stopbits = 1, bytesize = 8,timeout=0.1)
file  = open("log.log", "w")
#Connect to the serial modbus server
connection = client.connect()
#print connection
while 1:
#Starting add, num of reg to read, slave unit.
	#leituras = []

	for add in addresses:
		#print(add)
		try:
			#print(add)
			
			result = client.read_holding_registers(0x00,6,unit=add,timeout = 0.1)
			instant = [result.registers[0],result.registers[1]]	
			acumulado1 = [result.registers[2],result.registers[3]]	
			acumulado2 = [result.registers[4],result.registers[5]]	
			#instant = 1
			#acumulado1 = 2
			#acumulado2 = 3
			#print(result.registers)
			data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")			
			#print(data)
						
			decoder_instant = BinaryPayloadDecoder.fromRegisters(instant,
												 byteorder=Endian.Big,
												 wordorder=Endian.Big)
			decoder_acumulado1 = BinaryPayloadDecoder.fromRegisters(acumulado1,
												 byteorder=Endian.Big,
												 wordorder=Endian.Big)
			decoder_acumulado2 = BinaryPayloadDecoder.fromRegisters(acumulado2,
												 byteorder=Endian.Big,
												 wordorder=Endian.Big)
			

			#decoded = OrderedDict([
			#	('32float', decoder.decode_32bit_float()),
			#	('32float', decoder.decode_32bit_float()),
			#	('32float', decoder.decode_32bit_float())
		#	])

			#print("-" * 60)
		#	print("Decoded Data")
			#print("-" * 60)
			#print(decoded)
			dict = {
			'decoded_instant':decoder_instant.decode_32bit_float(),
			'decoded_acumulado1':decoder_acumulado1.decode_32bit_float(),
			'decoded_acumulado2':decoder_acumulado2.decode_32bit_float(),
			#'instant':instant,
			#'acumulado1':acumulado1,
			#'acumulado2':acumulado2,
			'address':add,
			'time':data
			}		
			file  = open("log.log", "a")
			json_string = json.dumps(dict)	
			file.write(json_string)
			file.write("\n")	
			file.close()			
			#leituras += [dict]	
			#for name, value in iteritems(decoded):
				#print("%s\t" % name, hex(value) if isinstance(value, int) else value)
		except:
			pass
		#print(dict)

#	file.print("n")
 		#print("error")
#Closes the underlying socket connection
#client.close()
