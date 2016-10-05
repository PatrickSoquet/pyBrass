# coding=utf-8
import sys
import time
from smbus import SMBus
# from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO


# P9_19: I2C2, SCL
# P9_20: I2C2, SDA
# i2cdetect -y -r 0
# i2cdetect -y -r 1

_DBG = True


class actuator:
	"""actuator class: control 6 EV + 2 pompes + melangeur + alarme, only 1 instance must be used!"""  # TODO mettre en static????
	# relay_state = 0x0000
	# relay state:				RB2       |       RB1
	#			  (msb) 1 1 1 1   1 1 1 1 | 1 1 1 1  1 1 1 1 (lsb)
	#                   a m r p   ev6 ev5 | ev4 ev3  ev2 ev1
	# a = alarm / m = melangeur / r = recirculateur cuve eau / p = pompe reverdoir
	# i2c = None  # SMBus()
	# relay 0 to 7
	RB1 = 0X20
	# relay 8 to F
	RB2 = 0x21


# !!!!! verifier que bit 1 => ferme et bit 0 ouvert sinon open_off et close_on!!!
	# A PRIORI OUI: car en NO!! =>
# note: si relay state bit a 1 => circuit FERME => le courant passe donc motor ON
# note: si relay state bit a 0 => circuit OUVERT => le courant ne passe pas donc  motor OFF
#NON FAUX________________________________________________________________
#  note : pour les EV on a donc 10 10 10 10 10 10 pour EV FERME => 0x0AAA
# note : pour les EV on a donc 01 01 01 01 01 01 pour EV OUVERTE => 0x0555
# note : 00 ou 11 interdit!! jamais de FF ou de 00!!!
# note : 0xF555 => tt ON + EV ouverte
# note : 0x0AAA => tt OFF + EV fermé
#VRAI!!!!!_______________________________________________________________
#  note : pour les EV on a donc 00 00 00 00 00 00 pour EV OUVERTE => 0x000
# note : pour les EV on a donc 11 11 11 11 11 11 pour EV FERME => 0xFFF
# note: 01 et 10 INTERDIT!!!!!!! jamais de AA ou de 55!!
# 0x0000 => tt on (ouvert et ON)
# 0xFFFF =>  tt off (fermé et OFF)
#
#attention: sans courant = etat 1!!! => si NC 1 et NO 0 si 0 =>  on inverse!!
#MODIF FAIRE => a tester de nouveau!!


	def __init__(self):
		self.relay_state = 0xFFFF #tt fermé et off
		try:
			self.i2c = SMBus(1)  # TODO debug possible??
		except:
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c actuator constructor not working "
			return
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c actuator constructor OK"
		return

	def open_on_all(self):
		# never use this API!!!! only for testing
		# open the 6 ev + on for the 3 motor + 1 alarm
		self.relay_state = 0x0000
		try:
			self.i2c.write_byte(self.RB1, self.relay_state & 0x00FF)
			self.i2c.write_byte(self.RB2, self.relay_state >> 8)
		except:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.write_byte not working!"
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')
		return "Ok"

	def close_off_all(self):
		# never use this API!!!!
		# close the 6 ev + off for the 3 motor + 1 alarm
		self.relay_state = 0xFFFF
		try:
			self.i2c.write_byte(self.RB1, self.relay_state & 0x00FF)
			self.i2c.write_byte(self.RB2, self.relay_state >> 8)
		except:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.write_byte not working!"
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')
		return "Ok"

	def ev_open_all(self):
		# open only the 6 ev
		self.relay_state = (0xF000 & self.relay_state) | 0x0000  #yes... just to not mix up everything
		try:
			self.i2c.write_byte(self.RB1, self.relay_state & 0x00FF)
			self.i2c.write_byte(self.RB2, self.relay_state >> 8)
		except:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.write_byte not working!"
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')  # TODO: afficher en binaire!!
		return "Ok"

	def ev_close_all(self):
		# close only the 6 ev
		self.relay_state = (0xF000 & self.relay_state) | 0x0FFF #yes again...
		try:
			self.i2c.write_byte(self.RB1, self.relay_state & 0x00FF)
			self.i2c.write_byte(self.RB2, self.relay_state >> 8)
		except:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.write_byte not working!"
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')
		return "Ok"

	def ev_close(self, evid, force=False):
		# close one of the ev : evid = 0..5 => put 2 bit to 1
		if evid > 5:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV number >5"
			return "ERROR"
		evtmp = (1 << evid * 2) + (1 << (evid * 2 + 1))
		if self.relay_state & evtmp == evtmp and not force:
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : ev " + str(evid) + " already close"
			return "noChange"
		else:
			self.relay_state |= evtmp
			if self.commit_state() == "ERROR":
				return "ERROR"
			if _DBG:
				print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : ev " + str(evid) + " closing"
				print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')
			return "Ok"

	def ev_open(self, evid, force=False):
		# open one of the ev : evid = 0..5
		if evid > 5:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV number >5"
			return "ERROR"
		evtmp = ~((1 << evid * 2) + (1 << (evid * 2 + 1)))
		if self.relay_state | evtmp == self.relay_state and not force:
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : ev " + str(evid) + " already open"
			return 'noChange'
		else:
			self.relay_state &= evtmp
			if self.commit_state() == "ERROR":
				return "ERROR"
			if _DBG:
				print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : ev " + str(evid) + " opening"
				print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : relay_state =" + format(self.relay_state, '#04x')
			return 'Ok'

	def pump_off(self, force=False):
		return self.prma_off(12, force)

	def pump_on(self, force=False):
		return self.prma_on(12, force)

	def recircul_off(self, force=False):
		return self.prma_off(13, force)

	def recircul_on(self, force=False):
		return self.prma_on(13, force)

	def mixer_off(self, force=False):
		return self.prma_off(14, force)

	def mixer_on(self, force=False):
		return self.prma_on(14, force)

	def alarm_off(self, force=False):
		return self.prma_off(15, force)

	def alarm_on(self, force=False):
		return self.prma_on(15, force)

	def prma_on(self, id_pow, force=False):   #ON = bit to 0!
		# call it only with the 8 functions above!!!
		# put off the selected actuator
		id = ~(1 << id_pow)
		if (self.relay_state & id) == id and not force:
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : prma " + str(id_pow) + " already on"
			return 'noChange'
		else:
			if self.commit_state() == "ERROR": return "ERROR"
			self.relay_state &= id
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : prma " + str(id_pow) + " turning on"
			return 'Ok'

	def prma_off(self, id_pow, force=False):  #ONFF = bit to 1!
		# call it only with the 8 functions above!!!
		# put on the selected actuator
		id = 1 << id_pow
		if (self.relay_state | id) == self.relay_state and not force:
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : prma " + str(id_pow) + " already off"
			return 'noChange'
		else:
			if self.commit_state() == "ERROR": return "ERROR"
			self.relay_state |= id
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : prma " + str(id_pow) + " turning off"
			return 'Ok'

	def ev_state(self, evid):  # from bit 0 to 12
		res1 = (self.relay_state & (1 << (evid * 2))) >> (evid * 2)
		res2 = (self.relay_state & (1 << (evid * 2 + 1))) >> (evid * 2 + 1)
		if res1 != res2:
			#should never happen but...
			print "__ERROR" + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(evid) + " state relay incoherent MAY LEAD TO SHORT CIRCUIT!!!"
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(evid) + " state is " + "close" if res1 else "open"
		return res1

	def pump_state(self):
		res = (self.relay_state & (1 << 12)) >> 12
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : pump state is " + ("off" if res else "on")
		return res

	def recircul_state(self):
		res = (self.relay_state & (1 << 13)) >> 13
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : recircul state is " + ("off" if res else "on")
		return res

	def mixer_state(self):
		res = (self.relay_state & (1 << 14)) >> 14
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : mixer state is " + ("off" if res else "on")
		return res

	def alarm_state(self):
		res = (self.relay_state & (1 << 15)) >> 15
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : alarm state is " + ("off" if res else "on")
		return res

	def commit_state(self):
		try:
			self.i2c.write_byte(self.RB1, self.relay_state & 0x00FF)
			self.i2c.write_byte(self.RB2, self.relay_state >> 8)
		except:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : i2c.write_byte not working!"
			return "ERROR"
		return 'Ok'


class pump:
	actuator = None

	def __init__(self, actu):
		self.actuator = actu
		return

	def on(self):
		return self.actuator.pump_on()

	def off(self):
		return self.actuator.pump_off()

	def getState(self):
		return self.actuator.pump_state()


class recircul:
	actuator = None

	def __init__(self, actu):
		self.actuator = actu
		return

	def on(self):
		return self.actuator.recircul_on()

	def off(self):
		return self.actuator.recircul_off()

	def getState(self):
		return self.actuator.recircul_state()


class mixer:
	actuator = None

	def __init__(self, actu):
		self.actuator = actu
		return

	def on(self):
		return self.actuator.mixer_on()

	def off(self):
		return self.actuator.mixer_off()

	def getState(self):
		return self.actuator.mixer_state()


class alarm:
	actuator = None
	msg = ""

	def __init__(self, actu):
		self.actuator = actu
		self.msg = ""
		return

	def on(self, msg):
		self.msg = msg
		return self.actuator.alarm_on()


	def off(self):
		self.msg = ""
		return self.actuator.alarm_off()

	def getState(self):
		return self.actuator.alarm_state()

	def getMsg(self):
		return self.msg

# TODO: attention tout vérifier avec la board: pas sur de la valeur des GPIO open/close = 0/1
# rappel débile: 0==False, tt le reste==True
class ev:
	"""base ElectroVanne class"""
	isOpen = 0
	isClose = 1
	# id = 0  # 0..5
	# gpio_open = 0
	# gpio_close = 0
	# actu = None

	def __init__(self, id, gpio_pin, actu):
		self.id = id
		self.gpio_open = gpio_pin[0]
		self.gpio_close = gpio_pin[1]
		self.actu = actu
		self.close(True)

	def getState(self):
		# verify just open == ~close...
		if bool(self.isOpen) != (not self.isClose):
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " close == open"
			return 'ERROR'
		return bool(self.isOpen)

	def check(self):

		# read the state of the EV and check if consistent with the isOpen/isClose + read the recorded state of the relay
		# be carefull : if done during the opening or closing of the EV it can be false!!!
		GPIO.setup(self.gpio_open, GPIO.IN)
		GPIO.setup(self.gpio_close, GPIO.IN)
		o = GPIO.input(self.gpio_open)
		c = GPIO.input(self.gpio_close)
		# TODO message de debug si erreur de lecture!!
		if o is None or c is None:
			print "__ERROR_HW " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " bugs cannot be read"
			return "ERROR"
		if o == c:
			if o:
				print "__ERROR_HW " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " bugs!!!! close AND open, verify HW!!!!"
				return "ERROR"
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " in incoherent state, still opening or closing, wait 2s"
			time.sleep(4)  # be carefull 4s is very long!!!!
			o = GPIO.input(self.gpio_open)
			c = GPIO.input(self.gpio_close)
			# TODO message de debug si erreur de lecture!!
			if o == c:
				print "__ERROR_HW " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " bugs!!!! EV BLOCKED, verify HW and EV!!!!"
				return "ERROR"
		if o != self.isOpen or c != self.isClose:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " incoherent state between state recorded (ev class)  and HW reading"
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " state reccorded(O/C): " + str(self.isOpen) + "/" + str(self.isClose) + " HW read: " + str(o) + "/" + str(c)
			return "ERROR"
		#now test the relay state recorded!! rel = True if open, False if not!
		rel = self.actu.ev_state(self.id)
		if rel != c:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " incoherent state between state recorded (actuator class)  and HW reading"
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " state reccorded: " + ("close" if rel else "open") + " HW read: " + ("close" if c else "open")
			return "ERROR"
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : EV " + str(self.id) + " check OK!  state = " + "close" if rel else "open"
		return 'Ok'

	def state_open(self):
		self.isOpen = 1
		self.isClose = 0
		return 'Ok'

	def state_close(self):
		self.isOpen = 0
		self.isClose = 1
		return 'Ok'

	def open(self):
		# open EV
		res = self.actu.ev_open(self.id)
		if res == 'ERROR': return res
		self.isOpen = 1
		self.isClose = 0
		return res

	def close(self, force=False):
		# close EV
		res = self.actu.ev_close(self.id, force)
		if res == 'ERROR': return res
		self.isOpen = 0
		self.isClose = 1
		return res


class evs:
	"""ev class: control 6 EV """
	# 6 EV objects
	#evsl = []  # [6]
	actu = None
	# constructor default value, can be modified
	# (gpio_pin_open,gpio_pin_close)
	GPIO_PINS = (("P8_11", "P8_12"), ("P8_13", "P8_14"), ("P8_15", "P8_16"), ("P8_17", "P8_18"), ("P8_19", "P9_25"), ("P9_27", "P9_28"))

	def __init__(self, actu):
		self.evsl = [None] * 6
		self.actu = actu
		for ii in range(0, 6):
			self.evsl[ii] = ev(ii, self.GPIO_PINS[ii], actu)
		return

	def open_all(self):
		res = self.actu.ev_open_all()
		if res != 'Ok': return res
		for ii in range(0, 6):
			self.evsl[ii].state_open()
		return 'Ok'

	def close_all(self):
		res = self.actu.ev_close_all()
		if res != 'Ok': return res
		for ii in range(0, 6):
			self.evsl[ii].state_close()
		return 'Ok'

	def check_all(self):
		checkOk = True
		for ii in range(0, 6):
			res = self.evsl[ii].check()
			if res != 'Ok': checkOk = False
		return checkOk

	def open(self, id):
		return self.evsl[id].open()

	def close(self, id):
		return self.evsl[id].close()

	def check(self, id):
		return self.evsl[id].check()

	def getStateAll(self):
		res = [None] * 6
		for ii in range(0, 6):
			r = self.evsl[ii].getState()
			if r == 'ERROR': return 'ERROR'
			res[ii] = r
		return res

	def getState(self, id):
		res = self.evsl[id].getState()
		if res == 'ERROR': return 'ERROR'
		return res
