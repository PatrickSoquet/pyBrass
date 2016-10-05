# coding=utf-8
# code exemple
# modbus1 = ModbusClient(host="192.168.0.7", unit_id=1, debug=True,auto_open=True, auto_close=True)
# debug peut etre a False
# modbus1.open()
# doit renvoyer True sinon c'est que ca ne marche pas!!
# modbus1.read_holding_registers(x,4)
# x: registre a lire
#   0: SV (redondant!)
#   1: HiAl
#   2: LoAl
#   7: P
#   8: I
#   9: D
# 4: nb de mot a lire TOUJOURS 4!! (PV|SV|ALM+MV|registre x)
# modbus1.write_single_register(x,val)
# x: registre a ecrire (x=0: SV par exemple)
# val: valeur a ecrire (word)
import sys


_TEST = False
if _TEST:
	from pyModbusTCP_TEST.client import ModbusClient
else:
	from pyModbusTCP.client import ModbusClient
#	try:
#		from pyModbusTCP.client import ModbusClient
#	except ImportError:
#		from pymodbus3.client.sync import ModbusTcpClient as ModbusClient

# debug mode configuration
_DBG = False
_PASS_ERROR = True

class pid:
	"""PID class: control 4 PID"""
	# this class control 4 PID, can be modified...
	# default value for the constructor, can be modified...
	PID_IP = "192.168.0.7"
	PID_ID = (1, 2, 3, 4)
	# default value for the PID value, can be modified
	# cuveau / cuve brass(non util) / reverdoir / cuvebu
	PID_SV = 0
	PID_HiAl = 200
	PID_LoAl = 10
	PID_P = 200
	PID_I = 0
	PID_D = 0

	modbus_debug = True
	# internal modbus access

	def __init__(self):
		self.pids = [None] * 4
		self.SV = [0] * 4
		self.temp = [0] * 4
		self.HiAl = [0] * 4
		self.LoAl = [0] * 4
		self.P = [0] * 4
		self.I = [0] * 4
		self.D = [0] * 4
		for ii in range(0, 4):
			self.pids[ii] = ModbusClient(host=self.PID_IP, unit_id=self.PID_ID[ii], debug=self.modbus_debug, auto_open=True, auto_close=True)
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : pids constructor OK"
		return

	def init_all_pid(self):
		for ii in range(0, 4):
			#print self.pids[ii].open()
			if not self.pids[ii].open():
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " connection cannot be opened"
				return "ERROR"
			ret = 0
			ret += self.pids[ii].write_single_register(0x00, self.PID_SV * 10)
			ret += self.pids[ii].write_single_register(0x01, self.PID_HiAl * 100)
			ret += self.pids[ii].write_single_register(0x02, self.PID_LoAl * 100)
			ret += self.pids[ii].write_single_register(0x07, self.PID_P)    # TODO : essayer de faire varier ce P!!!
			# ret += self.pids[ii].write_single_register(0x08, self.PID_I)
			# ret += self.pids[ii].write_single_register(0x09, self.PID_D) # note : pas la peine de les modifier a chaque fois...
			if ret != 4:
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single register on PID " + str(ii)
				return "ERROR"
			if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " initialized"

		self.SV = [self.PID_SV] * 4
		self.HiAl = [self.PID_HiAl] * 4
		self.LoAl = [self.PID_LoAl] * 4
		self.P = [self.PID_P] * 4
		self.I = [self.PID_I] * 4
		self.D = [self.PID_D] * 4
		return 'Ok'

	def read_all_temp_SV(self):
		temps = [[0] * 4, [0] * 4]
		for id in range(0, 4):
			if not self.pids[id].open():
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(id) + " connection cannot be opened"
				if _PASS_ERROR:
					return [[0] * 4, [0] * 4]
				else:
					return "ERROR"
			tmp = self.pids[id].read_holding_registers(0, 4)
			temps[0][id] = tmp[0]
			temps[1][id] = tmp[1]
			if temps[0][id] is None or temps[1][id] is None:
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(id)
				if _PASS_ERROR:
					return [[0] * 4, [0] * 4]
				else:
					return "ERROR"
			self.temp[id] = temps[0][id] / 100
			self.SV[id] = temps[1][id] / 10
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : temps & SVs = " + str(temps)
		return temps

	def read_all_temp(self):
		temps = [0] * 4
		for id in range(0, 4):
			if not self.pids[id].open():
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(id) + " connection cannot be opened"
				if _PASS_ERROR:
					return [0] * 4
				else:
					return "ERROR"
			temps[id] = self.pids[id].read_holding_registers(0, 4)[0] / 100
			if temps[id] is None:
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(id)
				if _PASS_ERROR:
					return [0] * 4
				else:
					return "ERROR"
			self.temp[id] = temps[id] / 100
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : temps = " + str(temps)
		return temps

	def read_all_SV(self):
		temps = [0] * 4
		for id in range(0, 4):
			if not self.pids[id].open():
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(id) + " connection cannot be opened"
				if _PASS_ERROR:
					return [0] * 4
				else:
					return "ERROR"
			temps[id] = self.pids[id].read_holding_registers(0, 4)[1]
			if temps[id] is None:
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(id)
				if _PASS_ERROR:
					return [0] * 4
				else:
					return "ERROR"
			self.SV[id] = temps[id] / 10
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : SVs = " + str(temps)
		return temps

	def read_temp(self, pid_id):
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			if _PASS_ERROR:
				return [0]
			else:
				return "ERROR"
		temps = self.pids[pid_id].read_holding_registers(0, 4)[0]
		if temps is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(pid_id)
			if _PASS_ERROR:
				return [0]
			else:
				return "ERROR"
		self.temp[pid_id] = temps / 100
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " temp = " + str(temps)
		return temps

	def read_SV(self, pid_id):
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		temps = self.pids[pid_id].read_holding_registers(0, 4)[1]
		if temps is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(pid_id)
			return "ERROR"
		self.SV[pid_id] = temps / 10
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " SV = " + str(temps)
		return temps

	def read_SV_temp(self, pid_id):
		temps = [0] * 2
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			if _PASS_ERROR:
				return [0] * 2
			else:
				return "ERROR"
		temps[0] = self.pids[pid_id].read_holding_registers(0, 4)[0]
		temps[1] = self.pids[pid_id].read_holding_registers(0, 4)[1]
		if temps[0] is None or temps[1] is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in read_holding_register on PID " + str(pid_id)
			if _PASS_ERROR:
				return [0] * 2
			else:
				return "ERROR"
		self.temp[pid_id] = temps[0] / 100
		self.SV[pid_id] = temps[1] / 10
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " temp & SV = " + str(temps)
		return temps

	# write SV value (targeted temp), register = 0x00
	def write_SV(self, pid_id, temp, force=False):
		if self.SV[pid_id] == temp and not force:
			if _DBG: print "__DEBUG " + 'no write_SV, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x00, temp * 10) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register SV on PID " + str(pid_id)
		self.SV[pid_id] = temp
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write SV = " + str(temp)
		return 'Ok'

	# write HighAlarm value (targeted temp), register = 0x01
	def write_HiAl(self, pid_id, temp, force=False):
		if self.HiAl[pid_id] == temp and not force:
			if _DBG: print 'no write_HiAl, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x01, temp * 100) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register HiAl on PID " + str(pid_id)
		self.HiAl[pid_id] = temp
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write HiAl = " + str(temp)
		return 'Ok'

	# write LowAlarm value (targeted temp), register = 0x02
	def write_LoAl(self, pid_id, temp, force=False):
		if self.LoAl[pid_id] == temp and not force:
			if _DBG: print 'no write_LoAl, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x02, temp * 100) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register LoAl on PID " + str(pid_id)
		self.LoAl[pid_id] = temp
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write LoAl = " + str(temp)
		return 'Ok'

	# write Proportional value, register = 0x07
	def write_P(self, pid_id, p_value, force=False):
		if self.P[pid_id] == p_value and not force:
			if _DBG: print 'no write_P, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x07, p_value) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register P on PID " + str(pid_id)
		self.P[pid_id] = p_value
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write P = " + str(p_value)
		return 'Ok'

	# write Integral value, register = 0x08
	def write_I(self, pid_id, i_value, force=False):
		if self.I[pid_id] == i_value and not force:
			if _DBG: print 'no write_I, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x08, i_value) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register I on PID " + str(pid_id)
		self.I[pid_id] = i_value
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write I = " + str(i_value)
		return 'Ok'

	# write Derivative value, register = 0x09
	def write_D(self, pid_id, d_value, force=False):
		if self.D[pid_id] == d_value and not force:
			if _DBG: print 'no write_P, old value is correct'
			return 'noChange'
		if not self.pids[pid_id].open():
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " connection cannot be opened"
			return "ERROR"
		if self.pids[pid_id].write_single_register(0x09, d_value) is None:
			print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : error in write_single_register D on PID " + str(pid_id)
		self.D[pid_id] = d_value
		if _DBG: print "__DEBUG " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(pid_id) + " write D = " + str(d_value)
		return 'Ok'

	#Check if class value and PID value are coherent!
	def checkAll(self):
		checkOk = True
		for ii in range(0, 4):
			if not self.pids[ii].open():
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " connection cannot be opened"
				return "ERROR"
			#note: temps vari, of course not to be controlled...
			reg1 = self.pids[ii].read_holding_registers(0x01, 4)
			reg2 = self.pids[ii].read_holding_registers(0x02, 4)
			reg7 = self.pids[ii].read_holding_registers(0x07, 4)
			reg8 = self.pids[ii].read_holding_registers(0x08, 4)
			reg9 = self.pids[ii].read_holding_registers(0x09, 4)
			if self.SV[ii] != reg1[1] / 10:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " SV false: PID SV = " + str(reg1[1]) + " / class SV = " + str(self.SV[ii])
			if self.HiAl[ii] != reg1[3] / 100:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " HiAl false: PID HiAl = " + str(reg1[3]) + " / class HiAl = " + str(self.HiAl[ii])
			if self.LoAl[ii] != reg2[3] / 100:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " LoAl false: PID LoAl = " + str(reg2[3]) + " / class LoAl = " + str(self.LoAl[ii])
			if self.P[ii] != reg7[3]:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " P false: PID P = " + str(reg7[3]) + " / class P = " + str(self.P[ii])
			if self.I[ii] != reg8[3]:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " I false: PID I = " + str(reg8[3]) + " / class I = " + str(self.I[ii])
			if self.D[ii] != reg9[3]:
				checkOk = False
				print "__ERROR " + self.__class__.__name__ + "." + sys._getframe().f_code.co_name + " : PID " + str(ii) + " D false: PID D = " + str(reg9[3]) + " / class D = " + str(self.D[ii])
		return checkOk

	def isReallyHeating(self, id):
		t = self.read_SV_temp(id)
		if t == 'ERROR': return t
		if t[0] < t[1]: return True
		else: return False

# for debug only!!!! should not be used by brass_process!!!!

	def _write_InP(self, id, param): # 21 : Pt100 / 22 Pt100 (-80..+300)
		return self.pids[id].write_single_register(0x0B, param)

	def _write_Ctrl(self,id,param): # 0 ONOFF / 1 APID / 5 nPID / 3 PoP 4 SoP
		return self.pids[id].write_single_register(0x06, param)

	def _write_Addr(self, id, param): # heu... marchera pas si on fait ca!!!
		return self.pids[id].write_single_register(0x16, param)

	def _write_AT(self, id, param): # autotune: 0: off 1: on 2 FoFF
		return self.pids[id].write_single_register(0x1D, param)

	def _write_Ctl(self, id, param): #temps entre chaque step du PID en unit: 0.1s
		return self.pids[id].write_single_register(0x1D, param)

	def _write_srun(self,id,param): #running status 0 run / 1 stop /2 hold -> note toujours en HolD car pas de running!!!!!!! c'est pas le P!!!
		return self.pids[id].write_single_register(0x1B, param)

	def _write_Sc(self,id,param): # ajustement! en 0.1°C
		return self.pids[id].write_single_register(0x10, param)

	def _write_AF(self,id,param):  # should be 128???
		return self.pids[id].write_single_register(0x10, param)

	def _read_version(self,id): #5180 pour AI-518 / 5187 AI-518P
		return self.pids[id].read_holding_registers(0x15, 4)[3]

	def _read_AF(self,id): #should be 128
		return self.pids[id].read_holding_registers(0x14, 4)[3]

	def _read_all(self,id):
		ll = []
		for ii in range(0, 40):
			ll += [self.pids[id].read_holding_registers(ii, 4)[3]]
		return ll
	#note : vérifier aussi que oP = 0 (SSR) / AF = 128