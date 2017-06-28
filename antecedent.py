class Antecedent:
	def __init__(self, key ="", val = ""):
		self.key = key
		self.val = val
		self.visited = False

	def display(self):
		print ("["+self.key+"] = " + self.val)

	def __str__(self):
		return "["+self.key+"] = " + self.val
