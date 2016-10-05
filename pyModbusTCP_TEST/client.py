import brass_process
import testpc

class ModbusClient:



	def __init__(self, host, unit_id, debug, auto_open, auto_close):
		self.id = unit_id   #1,2,3,4
		self.SV = 0
		return

	def open(self):
		return True

	def read_holding_registers(self, param, param1):
		# STUBS!!!! on renvoie toujours la valeur voulu pour les SV!!! (les temp ne sont pas lu en mode test)
		return [22, self.SV, 3, 4]

	def write_single_register(self, param1, param2):
		# STUBS!!!!
		if param1 == 0x00:
			self.SV = param2
		return True
