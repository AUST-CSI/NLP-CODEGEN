import Antecedent
from collections import Counter

generated = []

class Rule:
	def __init__(self, antecedent=[], consequent=[]):
		self.antecedent = antecedent
		self.consequent = consequent
	
	def reset(self):
	        self.antecedent = []
		self.consequent = []
	
	def display(self):
		print ("Antecedents: \n")
		for i in self.antecedent:
			i.display()		
		print ("Consequent: \n")
		for i in self.consequent:
			i.display()


	def getAntecedentSize(self):
		return len(antecedent)


	def generateCLIPSAction(self, no):
		res = "(defrule M" + str(no) +"\n\t\t"
		for i in self.antecedent:
			res = res + "(" + i.key + " " + i.val + ")\n\t\t"
		res = res + " => \n\t\t(printout t \""
		
		for i in self.consequent:
			res = res + i.val +" " 
		res = res + "\" crlf)\n\t\t(reset)\n)\n\n"
		return res
	
	@classmethod
	def getStartingPoint(self, rules):
		lst=[]
		for r in rules:
			for i in r.antecedent:
				lst.append(i.key)
		most_common,num_most_common = Counter(lst).most_common(1)[0] # 4, 6 times
		return most_common

	@classmethod
	def getAllowedValues(self, rules, key):
		values=[]
		for r in rules:
			for i in r.antecedent:
				if (i.key == key):
					values.append(i.val)
		return set(values)

	@classmethod
	def getOtherAntecedent(self, rules, key, val):
		lst = []
		flag=False
		index = 0
		for rule in rules:

			for antecedent in rule.antecedent:
				if(antecedent.key == key and antecedent.val == val):
					lst.append(key)
					lst.append(val)
					flag=True
					#print(antecedent.key)
				if(antecedent.key not in key and flag==True):
					#print(antecedent.key)				
					lst.append(antecedent.key)
					flag=False
					return lst
			if(flag == True):
				return None			
			index = index + 1

	@classmethod
	def generateCLIPSRules(self, rules, f):
		
		starting_point = Rule.getStartingPoint(rules)
		allowed_values = Rule.getAllowedValues(rules, starting_point)		
		f.write(Rule.generateQuestion(starting_point, allowed_values))
		f.write(Rule.generateCLIPSRule(starting_point,allowed_values))

		Rule.genAll(rules, starting_point,f)





	@classmethod
	def genAll(self, rules, key, f):
		allowedValues = Rule.getAllowedValues(rules, key)
		for val in allowedValues:
			ant = Rule.getOtherAntecedent(rules, key, val)
			if ant != None:
				allowed = Rule.getAllowedValues(rules, ant[2])
				f.write(Rule.generateQuestion(ant[2], allowed))
				f.write(Rule.generateCLIPSRule(ant[2], allowed, ant[0], ant[1]))
				Rule.genAll(rules, ant[2],f)



	@classmethod
	def generateQuestion(self, key, values):
		res = str("(deffunction get"+ key +"()\n(printout t " + key +": ")
		for i in values:
			res = res + i +" / "
		res = res + " crlf)\n(bind ?a (read))\n"
		res = res + "(while (and "
		for i in values:
			res = res + "(neq ?a " + i +")"
		res = res + ")\n"
		res = res + "\t(printout t "+key+": \"? plz enter "
		for i in values:
			res = res + i +" / "
		res = res +"\" crlf)\n\t(bind ?a (read)))\nreturn ?a)\n\n"
		return res

	@classmethod
	def generateCLIPSRule(self, key, values, dependency=None, dependency_val=None):
		generated.append(key)
		if(dependency == None):
			res = "(defrule " + key + "\n\t\t(not (" + key +" ?))\n\t\t=>\n\t\t"
			res = res + "(bind ?a (get" + key+"))\n\t\t(assert (" + key +" ?a)))\n\n\n"		
		else:
			res = "(defrule " + key + "\n\t\t(" + dependency + " " + dependency_val +")\n\t\t(not (" + key +" ?))\n\t\t=>\n\t\t"
			res = res + "(bind ?a (get" + key+"))\n\t\t(assert (" + key +" ?a)))\n\n\n"
		return res
		 
