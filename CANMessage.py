class Message:
	"""Class to organize the CAN data messages"""
	def __init__(self):
		self.time = 0
		self.port = 0
		self.hexID = 0
		self.data = [0x00]*8
		self.length = 0
		self.bitCount = 0
		self.decID = 0

	def importMessage(self,message = []):
		self.time = float(message[0])
		self.port = int(message[1])
		self.hexID = int(message[2], 16) # Converts the string of hex to an int
		self.data[7] = int(message[3], 16)
		self.data[6] = int(message[4], 16)
		self.data[5] = int(message[5], 16)
		self.data[4] = int(message[6], 16)
		self.data[3] = int(message[7], 16)
		self.data[2] = int(message[8], 16)
		self.data[1] = int(message[9], 16)
		self.data[0] = int(message[10], 16)
		self.length = int(message[11], 16)
		self.bitCount = int(message[12])
		self.decID = int(message[13])
	def combineBytes(self, start, stop):
		ret = 0
		offset = 0
		for i in range(stop, start+1):
			ret = (self.data[i] << offset) | ret
			offset = offset + 8
		return ret