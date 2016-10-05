# coding=utf-8
from smbus import SMBus
import Adafruit_BBIO.UART as UART
import serial
from time import sleep
import sys

# P9_19: I2C2, SCL
# P9_20: I2C2, SDA
# i2cdetect -y -r 0
# i2cdetect -y -r 1
_DBG = True
_PASS_ERROR = True

class sensor_ADC:
	"""root class for sensor connected to ADC"""
	# ADC address
	ADC_ADD = 0x68
	i2c = None  # SMBus(2)

	# config byte for each channel
	# channel 0 -> ultrasonic en volt pour cuve ebu
	#   0x98
	# channel 1 -> préssure en amp pour cuve ebu
	#   0xB9
	# channel 2 -> pressure en amp pour cuve eau
	#   0xD9
	CHANNEL = [0x98, 0xB9, 0xD9]

	def __init__(self):
		try:
			self.i2c = SMBus(1)  # TODO debug possible??
		except:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : sensor_ADC constructor not working "
			return
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : sensor_ADC constructor OK"
		return

	# CA MARCHE!!!! mais ya des trucs bizarre avec les adresses... normalement 98=channel 1, B9 le 2 et D9 le 3,
	# ce n est pas le cas... je lache l'affaire et il suffira de bien "regler" le code...
	def getVol(self, sensor_id):
		try:
			dataOut = self.i2c.read_i2c_block_data(self.ADC_ADD, self.CHANNEL[sensor_id],4) # bug bizarre!!!!!!!! il faut lire 2x avec une pause entre les 2 sinon ca marche pas...
			sleep(0.1)
			dataOut = self.i2c.read_i2c_block_data(self.ADC_ADD, self.CHANNEL[sensor_id],4)
		except:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c read error "
			return 'ERROR'
		# dataOUT = [HiByte,LoByte, bullshit, CHANNEL[sensor_id]]
		#if len(dataOut) != 4:
		if len(dataOut) < 4:  #!!! marchait avant mais maintenant je récupère 32 octets!!!!
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.read_i2c_block_data error, length must be 4, data read  = " + str(dataOut)
			return 'ERROR'
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : sensor " + str(sensor_id) + " = " + str(dataOut)
		level = dataOut[0] * 256 + dataOut[1]
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : sensor " + str(sensor_id) + " level = " + str(level)
		return level
		# argghh zut fallait write ou read??? voir le i2c.py et refaire les tests....


class s_reverdoir:
	"""sensor for reverdoir volume with serial connection"""

	# note: test with UART seems OK BUT: wait the TTL-RS232 converter to continue this!!
	# ser = None#serial.Serial()
	def __init__(self):
		UART.setup("UART4")
		# default values:
		# baudrate=9600, bytesize=EIGHTBITS,parity=PARITY_NONE,stopbits=STOPBITS_ONE,xonxoff=False...
		self.ser = serial.Serial(port="/dev/ttyO4", timeout=10)  # TODO ajust timeout... 10s is for test only! not usefull with the sensor?
		if not (self.ser.isOpen()):
			self.ser.close()
			self.ser.open()
			if not (self.ser.isOpen()):
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_reverdoir constructor not working!"
				return
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_reverdoir constructor ok"
		return

	# quel UART???
	# UART1 	P9_26 	P9_24 	P9_20 	P9_19 	/dev/ttyO1
	# UART2 	P9_22 	P9_21 					/dev/ttyO2
	# UART3 	P9_42 	P8_36 	P8_34 			/dev/ttyO3
	# UART4 	P9_11 	P9_13 	P8_35 	P8_33 	/dev/ttyO4
	# UART5 	P8_38 	P8_37 	P8_31 	P8_32 	/dev/ttyO5
	#
	# GPIO en P9: 25-27-28
	# touchscreen: 7-8-9-10-12-14-15-16- 19-20-21-22-23
	# I2C : 19-20 partagé avec le I2C du touchscreen...
	# =>UART4 : en 11-13
	# =>UART1 : en 24-26
	# mais UART 2 mort...

	def getRawVol(self):
		if not (self.ser.isOpen()):
			self.ser.close()
			self.ser.open()
			if not (self.ser.isOpen()):
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_reverdoir constructor not working!"
				return 'ERROR'
		self.ser.flushInput()
		dataIn = '$!RY0151\r\n'
		self.ser.write(dataIn)
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : write data = " + dataIn
		sleep(0.1)  # TODO a ajuster!!!!
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : waiting for data..."
		# dataOut = self.ser.readline()  # readline not working!!! why?
		dataOut = self.ser.read(14)
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : data read = " + str(dataOut) + "(data length = " + str(len(dataOut)) + ")"
		# dataOut ='*CFV0100AAAAB6' AAAA are the data
		if len(dataOut) != 14:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : wrong data length read, must be 14"
			if _PASS_ERROR:
				return 0
			else:
				return "ERROR"
		try:
			level = int(dataOut[8:10], 16) * 256 + int(dataOut[10:12], 16)
		except:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : serial.read error, data read are not convertible in int! " + str(dataOut[8:12])
			return 'ERROR'
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : data read level= " + str(level)
		return level

	def getVol(self):
		level = self.getRawVol()
		# TODO !!!! ICI FAIRE LA JOLIE CONVERSION!!!!!!! -> retourner le volume en litre! entre 0 et 10L, la c'est de la boucherie
		vol = level * 10 / 0xFFFF
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : volume read = " + str(
			vol) + "l"
		return vol

	def check(self):
		vol = self.getVol()
		if vol == 'ERROR': return False
		if 0 > vol > 10:
			return True
		else:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error reverdoir volume out of bound! vol =" + str(vol)
			return False


class s_cuveau:
	"""pressure sensor with analog intensity signal + ADC"""
	adc = None  # sensor_ADC()

	def __init__(self, adc):
		self.adc = adc
		return

	def getRawVol(self):
		level = self.adc.getVol(2)
		if level == 'ERROR': return level
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : data read level= " + str(level)
		return level

	def getVol(self):
		level = self.getRawVol()
		if level == 'ERROR':
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_cuveau ADC getVol error"
			if _PASS_ERROR:
				return 0
			else:
				return "ERROR"
		# TODO !!!! ICI FAIRE LA JOLIE CONVERSION!!!!!!! -> retourner le volume en litre! entre 0 et 75L
		vol = level * 75 / 0xFFFF  # 100 =nb de litre d'EAU (1l=1kg) pour la pression  max!! ca doit etre plus !!!
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : volume read = " + str(vol) + "l"
		return vol

	def check(self):
		vol = self.getVol()
		if vol == 'ERROR': return False
		if 0 > vol > 75:
			return True
		else:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error cuveau volume out of bound! vol = " + str(vol)
			return False


class s_cuvebu:
	"""ultrasonic sensor with analog volt signal + ADC and ressure sensor with analog intensity signal + ADC"""
	adc = None  # sensor_ADC()

	def __init__(self, adc):
		self.adc = adc
		return

	def getRawVol(self):
		level = self.adc.getVol(0)
		if level == 'ERROR': return level
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : data read level= " + str(level)
		return level

	def getVol(self):
		level = self.getRawVol()
		if level == 'ERROR':
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_cuvebu ADC getVol error"
			if _PASS_ERROR:
				return 0
			else:
				return "ERROR"
		# TODO !!!!! ICI FAIRE LA JOLIE CONVERSION!!!!!!! -> retourner le volume en litre! entre 0 et 75L !!
		# input : entre 0 et 65535 en theorie mais a etalonner! attention : etalonner avec les input du bidule
		# (note: super chiant ca!!!! je ne vais mettre des relais pour ca!!! des boutons manuels? y reflechir...
		# faut un bouton 3 position "teach IN" branche a : U+/rien/U-) => acheter un bete swith 3 positions?
		# finalement: etalonnage a la mano...
		# MIN = 29200 = 0l
		# MAX = 426 = 75l
		# => formule = 75 - 0.00397*level!!
		vol = 75 - level * 0.0026
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : volume read = " + str(vol) + "l"
		return vol

	def getRawWeight(self):
		level = self.adc.getVol(1)
		if level == 'ERROR': return level
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : data read level= " + str(level)
		return level

	def getWeight(self):
		level = self.getRawWeight()
		if level == 'ERROR':
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : s_cuvebu ADC getWeight error"
			if _PASS_ERROR:
				return 0
			else:
				return "ERROR"

		# TODO !!!! ICI FAIRE LA JOLIE CONVERSION!!!!!!! -> retourner le poids en kg entre 0 et 85kg
		# input : entre 0 et 65535 en theorie mais a etalonner!
		wei = level * 200 / 0xFFFF  # 200 = nb de litre pour la pression  max!! ca doit etre plus !!!
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : weight read = " + str(wei) + "kg"
		return wei

	def getDensity(self):
		# return the density in gravity nominal -> between 1.000 and 1.150
		res = self.getVol() / self.getWeight()
		if _DBG: print "__DEBUG" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : density read = " + str(res)
		return res

	def check(self):
		vol = self.getVol()
		if vol == 'ERROR': return False
		if 0 <= vol < 75:
			pass
		else:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error cuvebu volume out of bound! vol =" + str(vol)
			return False
		wei = self.getWeight()
		if wei == 'ERROR': return False
		if 0 <= wei < 200:
			return True
		else:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error cuvebu weight out of bound! weiight =" + str(wei)
			return False
