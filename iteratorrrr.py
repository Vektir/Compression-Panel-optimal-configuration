a=[]
def getstuff():
	for type1 in range(7):
		for type2 in range(7-type1):
			for type3 in range(7-type1-type2):
				type4 = 6 - type1 - type2 - type3
				b=[]
				for i in range(type1):
					b.append(1)
				for i in range(type2):
					b.append(2)
				for i in range(type3):
					b.append(3)
				for i in range(type4):
					b.append(4)
				a.append(b)

	for type1 in range(8):
		for type2 in range(8-type1):
			for type3 in range(8-type1-type2):
				type4 = 7 - type1 - type2 - type3
				b=[]
				for i in range(type1):
					b.append(1)
				for i in range(type2):
					b.append(2)
				for i in range(type3):
					b.append(3)
				for i in range(type4):
					b.append(4)
				a.append(b)

	for type1 in range(9):
		for type2 in range(9-type1):
			for type3 in range(9-type1-type2):
				type4 = 8 - type1 - type2 - type3
				b=[]
				for i in range(type1):
					b.append(1)
				for i in range(type2):
					b.append(2)
				for i in range(type3):
					b.append(3)
				for i in range(type4):
					b.append(4)
				a.append(b)
	return a
#print(getstuff())