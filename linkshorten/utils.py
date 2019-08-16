from string import digits, ascii_lowercase, ascii_uppercase

class Convert():
	def __init__(self, n):
		self.base = digits + ascii_lowercase + ascii_uppercase
		self.n = n
	
	def toBase10(self):
		b10 = 0
		for i in range(len(self.n)):
			b10 = 62 * b10 + self.base.find(self.n[i])
		return b10

	def toBase62(self):
		if self.n > 0:
			base62 = list()
			while self.n != 0:
				self.n, i = divmod(self.n, 62)
				base62.append(self.base[i])
			return ''.join(reversed(base62))
		elif self.n == 0:
			return '0'
		else:
			return False