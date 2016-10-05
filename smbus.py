class SMBus:
	nothing = 0

	def __init__(self, aa):
		self.nothing = aa
		return

	def read_i2c_block_data(self, a, b, c):
		return [0x70, 0x70, 0x70, 0x70]

	def write_byte(self, address, param):
		pass
